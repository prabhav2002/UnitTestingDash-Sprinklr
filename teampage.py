# importing libraries
from elasticsearch import Elasticsearch
from datetime import datetime as dt
from datetime import date
import pandas as pd
import plotly.express as px
from dateutil.relativedelta import relativedelta

# connecting with elasticsearch server
es = Elasticsearch()

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


# fucntion to plot pie-chart of team-wise developer count.
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


# function plot count of testcases vs time for selected teams for selected date-range
# selection for date-wise, week-wise, month-wise aggregation
# selection for type of testcases: added, deleted, effective
def teampage_row3(timePeriod, teamNamesMultiDropdown, testCaseType, startdate, enddate):
    if type(teamNamesMultiDropdown) == str:
        teamNamesMultiDropdown = [teamNamesMultiDropdown]

    # setting testcase-type
    if testCaseType == "Effective Test Cases":
        caseTypeString = "effectiveCount"
    elif testCaseType == "Test Cases Added":
        caseTypeString = "testAdded"
    elif testCaseType == "Test Cases Deleted":
        caseTypeString = "testDeleted"

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
            "aggs": {
                "date": {
                    "date_histogram": {
                        "field": "fromTime",
                        "interval": "day",
                        "format": "yyyy-MM-dd",
                    },
                    "aggs": {"Total": {"sum": {"field": caseTypeString}}},
                }
            },
        }
        res = es.search(index="unit_test_tracker", body=query_filter)
        for j in res["aggregations"]["date"]["buckets"]:
            teamName = i
            testCaseCount = j["Total"]["value"]
            # converting timezone to Asia/Kolkata
            timestamp = j["key"] + 66600000
            date_time = dt.fromtimestamp(int(timestamp) / 1000)
            data.append([date_time, testCaseCount, teamName])

    # creating dataframe
    df = pd.DataFrame(data, columns=["Date", "TestCaseCount", "Team"])

    # aggregated date-wise and plotting of data
    if timePeriod == "Date-wise Aggregation":
        fig = px.bar(
            df,
            x="Date",
            y="TestCaseCount",
            color="Team",
            title="Team-wise " + testCaseType,
            height=900,
            width=1100,
        )
        # range slider option
        start_date_plus_month = start_date_object + relativedelta(months=1)
        fig.update_xaxes(
            rangeslider_visible=True,
            range=[start_date_object, min(start_date_plus_month, end_date_object)],
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
        fig.update_yaxes(title=testCaseType)
        return fig

    # aggregated week-wise and plotting of data
    elif timePeriod == "Week-wise Aggregation":
        dfWeek = df.copy()
        dfWeek = (
            dfWeek.groupby(["Team", pd.Grouper(key="Date", freq="W-SUN")])[
                ("TestCaseCount")
            ]
            .sum()
            .reset_index()
            .sort_values("Date")
        )
        dfWeek["Date"] = dfWeek["Date"].dt.strftime("%W")
        dfWeek.rename(columns={"Date": "Week"}, inplace=True)
        fig = px.bar(
            dfWeek,
            x="Week",
            y="TestCaseCount",
            color="Team",
            title="Team-wise " + testCaseType,
            height=900,
            width=1100,
        )
        fig.update_xaxes(title="Week Number of the Year", rangeslider_visible=True)
        fig.update_yaxes(title=testCaseType)
        return fig

    # aggregated month-wise and plotting of data
    else:
        dfMonth = df.copy()
        dfMonth = (
            dfMonth.groupby(["Team", pd.Grouper(key="Date", freq="1M")])[
                ("TestCaseCount")
            ]
            .sum()
            .reset_index()
            .sort_values("Date")
        )
        dfMonth["Date"] = dfMonth["Date"].dt.strftime("%B")
        dfMonth.rename(columns={"Date": "Month"}, inplace=True)
        fig = px.bar(
            dfMonth,
            x="Month",
            y="TestCaseCount",
            color="Team",
            title="Team-wise " + testCaseType,
            height=900,
            width=1100,
        )
        fig.update_xaxes(title="Month", rangeslider_visible=True)
        fig.update_yaxes(title=testCaseType)
        return fig


# plot the stats of developers of the selected team in selected date range
def teampage_row4(team, testCaseType, startdate, enddate):
    # setting testcase-type
    if testCaseType == "Effective Test Cases":
        caseTypeString = "effectiveCount"
    elif testCaseType == "Test Cases Added":
        caseTypeString = "testAdded"
    elif testCaseType == "Test Cases Deleted":
        caseTypeString = "testDeleted"

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
                "aggs": {"testCaseCount": {"sum": {"field": caseTypeString}}},
            },
        },
    }
    res = es.search(index="unit_test_tracker", body=query_filter)

    # saving result to data
    for j in res["aggregations"]["dev"]["buckets"]:
        devName = j["key"]
        count = j["testCaseCount"]["value"]
        data.append([devName, count])

    # creating dataframe and sorting it by Email field
    df = pd.DataFrame(data, columns=["Email", "Test Case Count"])
    df = df.sort_values("Email")

    # plot
    fig = px.bar(
        df,
        x="Email",
        y="Test Case Count",
        title="Total " + testCaseType + " by Developers (Team: " + team + " )",
        height=900,
        width=1100,
    )
    return fig
