# importing libraries
from elasticServerDashApp import elasitcServerDashApp
from datetime import datetime as dt
from datetime import date
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dateutil.relativedelta import relativedelta

# connecting with elasticsearch server
es = elasitcServerDashApp()


# function get total numbers of team and name of those teams
def teampage_row1():
    # aggregation to get all the teams
    query_filter = {
        "size": 0,
        "aggs": {
            "team": {"terms": {"field": "cloudName.keyword", "size": 2147483647}},
        },
    }
    result = es.search(index="unit_test_tracker", body=query_filter)

    # saving result to teamSet so that we will get all the unique teams
    teamSet = set()
    for i in result["aggregations"]["team"]["buckets"]:
        team = i["key"]
        teamSet.add(team)
    teamList = list(teamSet)
    teamList.sort()
    return len(teamSet), teamList


# function to plot pie-chart of team-wise developer count.
def teampage_row2():
    teams, teamList = teampage_row1()
    data = []
    # teamwise querying in for loop to get the number of distinct developers of that team
    for i in teamList:
        query_filter = {
            "size": 0,
            "query": {
                "term": {
                    "cloudName.keyword": {
                        "value": i,
                    }
                }
            },
            "aggs": {"dev": {"cardinality": {"field": "email.keyword"}}},
        }
        res = es.search(index="unit_test_tracker", body=query_filter)
        # saving result to data list
        data.append([i, res["aggregations"]["dev"]["value"]])

    dfChart = pd.DataFrame(data, columns=["teamName", "devCountPerTeam"])
    dfChart = dfChart.sort_values(by="teamName")
    fig = px.pie(
        dfChart,
        values="devCountPerTeam",
        names="teamName",
        hole=0.3,
        title="<b>Number of Developers per Team<b>",
    )
    return fig


# function plot count of testcases vs time for selected teams, get JSONfied data for selected date-range
# selection for date-wise, week-wise, month-wise aggregation
# selection for type of testcases: added, deleted, effective
def teampage_row3(timePeriod, teamNamesMultiDropdown, testCaseType, startdate, enddate):

    if teamNamesMultiDropdown == []:
        data = []
        dfTeamNone = pd.DataFrame(data, columns=[])
        fig = go.Figure()
        return fig, dfTeamNone.to_json(orient="split")

    if type(teamNamesMultiDropdown) == str:
        teamNamesMultiDropdown = [teamNamesMultiDropdown]

    # converting startdate, enddate to timestamp
    start_date_object = date.fromisoformat(startdate)
    end_date_object = date.fromisoformat(enddate)

    data = []
    # query to get count selected testcase type date-wise aggregated for selected teams
    for i in teamNamesMultiDropdown:
        query_filter = {
            "size": 0,
            "query": {
                "bool": {
                    "must": [
                        {"match": {"cloudName.keyword": i}},
                    ],
                    # filter to get the results of selected date range only
                    "filter": [
                        {
                            "range": {
                                "fromTime": {
                                    "time_zone": "+05:30",
                                    "gte": start_date_object,
                                    "lte": end_date_object,
                                }
                            }
                        }
                    ],
                }
            },
            # summation of date-wise aggregation of every test case type
            "aggs": {
                "date": {
                    "date_histogram": {
                        "field": "fromTime",
                        "interval": "day",
                        "format": "yyyy-MM-dd",
                    },
                    "aggs": {
                        "DatewiseEffective": {"sum": {"field": "effectiveCount"}},
                        "DatewiseAdded": {"sum": {"field": "testAdded"}},
                        "DatewiseDeleted": {"sum": {"field": "testDeleted"}},
                    },
                }
            },
        }
        res = es.search(index="unit_test_tracker", body=query_filter)
        for j in res["aggregations"]["date"]["buckets"]:
            teamName = i
            effective_count = j["DatewiseEffective"]["value"]
            test_added = j["DatewiseAdded"]["value"]
            test_deleted = j["DatewiseDeleted"]["value"]
            # converting timezone to Asia/Kolkata
            timestamp = j["key"] + 86400000
            date_time = dt.fromtimestamp(int(timestamp) / 1000)
            data.append(
                [date_time, teamName, effective_count, test_added, test_deleted]
            )

    # creating dataframe
    dfTeam = pd.DataFrame(
        data,
        columns=[
            "Date",
            "Team",
            "Effective Test Cases",
            "Test Cases Added",
            "Test Cases Deleted",
        ],
    )

    if dfTeam.shape[0] == 0:
        dataNone = []
        dfNone = pd.DataFrame(dataNone, columns=[])
        fig = go.Figure()
        fig.update_layout(
            xaxis={"visible": False},
            yaxis={"visible": False},
            annotations=[
                {
                    "text": "Sorry... Nothing to plot with the selected filters!",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {"size": 28},
                }
            ],
        )
        return fig, dfNone.to_json(orient="split")

    # aggregated date-wise and plotting of data
    if timePeriod == "Daily":
        fig = px.bar(
            dfTeam,
            x="Date",
            y=testCaseType,
            color="Team",
            title="Team-wise " + testCaseType + " (Daily)",
            height=900,
            width=1100,
        )
        # range slider option
        start_date_plus_month = start_date_object + relativedelta(months=1)
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=7, label="1w", step="day", stepmode="backward"),
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
        )
        if dfTeam.shape[0] > 1:
            fig.update_xaxes(
                range=[
                    start_date_object,
                    min(end_date_object, start_date_plus_month),
                ]
            )
        fig.update_yaxes(title=testCaseType)
        return fig, dfTeam.to_json(orient="split")

    # aggregated week-wise and plotting of data
    elif timePeriod == "Weekly":
        dfWeek = dfTeam.copy()
        dfWeek = (
            dfWeek.groupby(["Team", pd.Grouper(key="Date", freq="W-SUN")])[
                [
                    "Effective Test Cases",
                    "Test Cases Added",
                    "Test Cases Deleted",
                ]
            ]
            .sum()
            .reset_index()
        )
        dfWeek["Date"] = dfWeek["Date"].dt.strftime("%W, %Y")
        dfWeek.rename(columns={"Date": "Week Number of the Year"}, inplace=True)
        fig = px.bar(
            dfWeek,
            x="Week Number of the Year",
            y=testCaseType,
            color="Team",
            title="Team-wise " + testCaseType + " (Weekly)",
            height=900,
            width=1100,
        )
        fig.update_xaxes(title="Week Number of the Year", rangeslider_visible=True)
        fig.update_yaxes(title=testCaseType)
        return fig, dfWeek.to_json(orient="split")

    # aggregated month-wise and plotting of data
    else:
        dfMonth = dfTeam.copy()
        dfMonth = (
            dfMonth.groupby(["Team", pd.Grouper(key="Date", freq="1M")])[
                [
                    "Effective Test Cases",
                    "Test Cases Added",
                    "Test Cases Deleted",
                ]
            ]
            .sum()
            .reset_index()
        )
        dfMonth["Date"] = dfMonth["Date"].dt.strftime("%b, %Y")
        dfMonth.rename(columns={"Date": "Month"}, inplace=True)
        fig = px.bar(
            dfMonth,
            x="Month",
            y=testCaseType,
            color="Team",
            title="Team-wise " + testCaseType + " (Monthly)",
            height=900,
            width=1100,
        )
        fig.update_xaxes(title="Month", rangeslider_visible=True)
        fig.update_yaxes(title=testCaseType)
        return fig, dfMonth.to_json(orient="split")


# plot the stats of developers and get JSONfied data of the selected team in selected date range
def teampage_row4(team, testCaseType, startdate, enddate):

    # converting startdate, enddate to timestamp
    start_date_object = date.fromisoformat(startdate)
    end_date_object = date.fromisoformat(enddate)

    data = []
    # query to get count of given testcase type developer wise for selected team
    query_filter = {
        "size": 0,
        "query": {
            "bool": {
                "must": [
                    {"match": {"cloudName.keyword": team}},
                ],
                # filter to get the results of selected date range only
                "filter": [
                    {
                        "range": {
                            "fromTime": {
                                "time_zone": "+05:30",
                                "gte": start_date_object,
                                "lte": end_date_object,
                            }
                        }
                    }
                ],
            }
        },
        # aggregation to find count of selected type of test cases of every developer of the team
        "aggs": {
            "dev": {
                "terms": {"field": "email.keyword", "size": 2147483647},
                "aggs": {
                    "DatewiseEffective": {"sum": {"field": "effectiveCount"}},
                    "DatewiseAdded": {"sum": {"field": "testAdded"}},
                    "DatewiseDeleted": {"sum": {"field": "testDeleted"}},
                },
            },
        },
    }
    res = es.search(index="unit_test_tracker", body=query_filter)

    # saving result to data
    for j in res["aggregations"]["dev"]["buckets"]:
        devName = j["key"]
        effective_count = j["DatewiseEffective"]["value"]
        test_added = j["DatewiseAdded"]["value"]
        test_deleted = j["DatewiseDeleted"]["value"]
        data.append([devName, effective_count, test_added, test_deleted])

    # creating dataframe and sorting it by Email field
    df = pd.DataFrame(
        data,
        columns=[
            "Email",
            "Effective Test Cases",
            "Test Cases Added",
            "Test Cases Deleted",
        ],
    )
    df = df.sort_values("Email")

    if df.shape[0] == 0:
        fig = go.Figure()
        fig.update_layout(
            xaxis={"visible": False},
            yaxis={"visible": False},
            annotations=[
                {
                    "text": "Sorry... Nothing to plot with the selected filters!",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {"size": 28},
                }
            ],
        )
        return fig, df.to_json(orient="split")

    # plot
    fig = px.bar(
        df,
        x="Email",
        y=testCaseType,
        title="Total " + testCaseType + " by Developers (Team: " + team + " )",
        height=900,
        width=1100,
    )
    return fig, df.to_json(orient="split")
