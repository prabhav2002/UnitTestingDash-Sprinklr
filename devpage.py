# importing libraries
from elasticServerDashApp import elasitcServerDashApp
from datetime import datetime as dt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
from dateutil.relativedelta import relativedelta
import sys

# connecting with elasticsearch server
es = elasitcServerDashApp()

# function get list of all developers in the provided data
def devpage_row1():
    # aggregation to get all developers
    query_filter = {
        "size": 0,
        "aggs": {"dev": {"terms": {"field": "email.keyword", "size": 2147483647}}},
    }
    result = es.search(index="unit_test_tracker", body=query_filter)

    devEmailSet = set()
    for i in result["aggregations"]["dev"]["buckets"]:
        dev = i["key"]
        devEmailSet.add(dev)
    devEmailList = list(devEmailSet)
    devEmailList.sort()
    return devEmailList


# function to get team-name of developer, get total testcases added, deleted, effective in the selected date-range
def devpage_row2(givenEmailID, startdate, enddate):
    if givenEmailID == None:
        return "Enter the Sprinklr Mail ID above to see the team...", 0, 0, 0
    else:

        # converting startdate, enddate to timestamp
        start_date_object = date.fromisoformat(startdate)
        end_date_object = date.fromisoformat(enddate)

        # query to get date-wise aggregated count for testcases added, deleted, effective for selected developer in the given date range
        query = {
            "size": 0,
            "query": {
                "bool": {
                    "must": [
                        {"match": {"email.keyword": givenEmailID}},
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
                "DevwiseEffective": {"sum": {"field": "effectiveCount"}},
                "DevwiseAdded": {"sum": {"field": "testAdded"}},
                "DevwiseDeleted": {"sum": {"field": "testDeleted"}},
            },
        }

        res = es.search(index="unit_test_tracker", body=query)

        # taking effectiveTestCases, testCasesAdded and testCasesDeleted from the result
        effectiveTestCases = res["aggregations"]["DevwiseEffective"]["value"]
        testCasesAdded = res["aggregations"]["DevwiseAdded"]["value"]
        testCasesDeleted = res["aggregations"]["DevwiseDeleted"]["value"]

        # query to get team name of selected developer
        query = {
            "size": 0,
            "query": {
                "term": {
                    "email.keyword": {
                        "value": givenEmailID,
                    }
                }
            },
            "aggs": {
                "Teams": {"terms": {"field": "cloudName.keyword", "size": 2147483647}},
            },
        }

        result = es.search(index="unit_test_tracker", body=query)

        # taking teamNameSet from the result
        teamNameSet = set()
        for i in result["aggregations"]["Teams"]["buckets"]:
            teamName = i["key"]
            teamNameSet.add(teamName)

        teamNameList = list(teamNameSet)
        teamNameString = str(teamNameList[0])
        for i in range(1, len(teamNameList)):
            teamNameString += ", " + str(teamNameList[i])

        return teamNameString, effectiveTestCases, testCasesAdded, testCasesDeleted


# function plot count of testcases vs time for selected developer for selected date-range
# and get JSONfied data as output
# selection for daily, weekly, monthly aggregation
# selection for type of testcases: added, deleted, effective
def devpage_row3(timePeriod, testCaseType, givenEmailID, startdate, enddate):
    if givenEmailID == None:
        data = []
        dfDevNone = pd.DataFrame(data, columns=[])
        fig = go.Figure()
        fig.update_layout(
            xaxis={"visible": False},
            yaxis={"visible": False},
            annotations=[
                {
                    "text": "Select the Mail ID to see the plot!",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {"size": 28},
                }
            ],
        )
        return fig, dfDevNone.to_json(orient="split")
    else:

        # converting startdate, enddate to timestamp
        start_date_object = date.fromisoformat(startdate)
        end_date_object = date.fromisoformat(enddate)

        # query to get count of test cases date-wise aggregated for selected developer in the selected date range
        query_filter = {
            "size": 0,
            "query": {
                "bool": {
                    "must": [
                        {"match": {"email.keyword": givenEmailID}},
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
                    "aggs": {
                        "DatewiseEffective": {"sum": {"field": "effectiveCount"}},
                        "DatewiseAdded": {"sum": {"field": "testAdded"}},
                        "DatewiseDeleted": {"sum": {"field": "testDeleted"}},
                    },
                }
            },
        }
        res = es.search(index="unit_test_tracker", body=query_filter)
        data = []
        for i in res["aggregations"]["date"]["buckets"]:
            effective_count = i["DatewiseEffective"]["value"]
            test_added = i["DatewiseAdded"]["value"]
            test_deleted = i["DatewiseDeleted"]["value"]
            # converting timezone to Asia/Kolkata
            timestamp = i["key"] + 86400000
            date_time = dt.fromtimestamp(int(timestamp) / 1000)
            data.append([date_time, effective_count, test_added, test_deleted])

        # creating dataframe
        dfDev = pd.DataFrame(
            data,
            columns=[
                "Date",
                "Effective Test Cases",
                "Test Cases Added",
                "Test Cases Deleted",
            ],
        )

        if dfDev.shape[0] == 0:
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
                dfDev,
                x="Date",
                y=testCaseType,
                title=testCaseType + " by " + givenEmailID + " (Daily)",
                height=900,
                width=1100,
            )
            start_date_plus_fourmonths = start_date_object + relativedelta(months=4)
            fig.update_xaxes(
                rangeslider_visible=True,
                # range slider option
                rangeselector=dict(
                    buttons=list(
                        [
                            dict(count=7, label="1w", step="day", stepmode="backward"),
                            dict(
                                count=1, label="1m", step="month", stepmode="backward"
                            ),
                            dict(step="all"),
                        ]
                    )
                ),
            )
            if dfDev.shape[0] > 1:
                fig.update_xaxes(
                    range=[
                        start_date_object,
                        min(end_date_object, start_date_plus_fourmonths),
                    ]
                )
            fig.update_yaxes(title=testCaseType)
            return fig, dfDev.to_json(orient="split")

        # aggregated week-wise and plotting of data
        elif timePeriod == "Weekly":
            dfWeek = dfDev.copy()
            dfWeek = (
                dfWeek.groupby([pd.Grouper(key="Date", freq="W-SUN")])[
                    [
                        "Effective Test Cases",
                        "Test Cases Added",
                        "Test Cases Deleted",
                    ]
                ]
                .sum()
                .reset_index()
                .sort_values("Date")
            )
            dfWeek["Date"] = dfWeek["Date"].dt.strftime("%W, %Y")
            dfWeek.rename(columns={"Date": "Week Number of the Year"}, inplace=True)
            fig = px.bar(
                dfWeek,
                x="Week Number of the Year",
                y=testCaseType,
                title=testCaseType + " by " + givenEmailID + " (Weekly)",
                height=900,
                width=1100,
            )
            fig.update_xaxes(title="Week Number of the Year", rangeslider_visible=True)
            fig.update_yaxes(title=testCaseType)
            return fig, dfWeek.to_json(orient="split")

        # aggregated month-wise and plotting of data
        else:
            dfMonth = dfDev.copy()
            dfMonth = (
                dfMonth.groupby([pd.Grouper(key="Date", freq="1M")])[
                    [
                        "Effective Test Cases",
                        "Test Cases Added",
                        "Test Cases Deleted",
                    ]
                ]
                .sum()
                .reset_index()
                .sort_values("Date")
            )
            dfMonth["Date"] = dfMonth["Date"].dt.strftime("%b, %Y")
            dfMonth.rename(columns={"Date": "Month"}, inplace=True)
            fig = px.bar(
                dfMonth,
                x="Month",
                y=testCaseType,
                title=testCaseType + " by " + givenEmailID + " (Monthly)",
                height=900,
                width=1100,
            )
            fig.update_xaxes(title="Month", rangeslider_visible=True)
            fig.update_yaxes(title=testCaseType)
            return fig, dfMonth.to_json(orient="split")


# function to plot comparison between two developers for given date-range
# selection for testcase type: added, deleted, effective
def devpage_row4(givenEmailID1, givenEmailID2, testCaseType, startdate, enddate):
    if givenEmailID1 == None:
        fig = go.Figure()
        fig.update_layout(
            xaxis={"visible": False},
            yaxis={"visible": False},
            annotations=[
                {
                    "text": "Select the Mail IDs to see the plot!",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {"size": 28},
                }
            ],
        )
        return fig
    elif givenEmailID2 == None:
        fig = go.Figure()
        fig.update_layout(
            xaxis={"visible": False},
            yaxis={"visible": False},
            annotations=[
                {
                    "text": "Select the Mail IDs to see the plot!",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {"size": 28},
                }
            ],
        )
        return fig
    else:
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

        # query to get count of given testcase type aggregated date-wise for first selected developer in the selected date range
        query_filter = {
            "size": 0,
            "query": {
                "bool": {
                    "must": [
                        {"match": {"email.keyword": givenEmailID1}},
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
        data1 = []
        for i in res["aggregations"]["date"]["buckets"]:
            testCaseCount = i["Total"]["value"]
            # converting timezone to Asia/Kolkata
            timestamp = i["key"] + 86400000
            date_time = dt.fromtimestamp(int(timestamp) / 1000)
            data1.append([date_time, testCaseCount])

        # query to get count of given testcase type aggregated date-wise for second selected developer in the selected date range
        query_filter = {
            "size": 0,
            "query": {
                "bool": {
                    "must": [
                        {"match": {"email.keyword": givenEmailID2}},
                    ],
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
        data2 = []
        for i in res["aggregations"]["date"]["buckets"]:
            testCaseCount = i["Total"]["value"]
            # converting timezone to Asia/Kolkata
            timestamp = i["key"] + 86400000
            date_time = dt.fromtimestamp(int(timestamp) / 1000)
            data2.append([date_time, testCaseCount])

        # creating two dataframes from the data we got
        df1 = pd.DataFrame(data1, columns=["Date", testCaseType])
        df2 = pd.DataFrame(data2, columns=["Date", testCaseType])

        if df1.shape[0] == 0 and df2.shape[0] == 0:
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
            return fig

        start_date_plus_twomonths = start_date_object + relativedelta(months=2)

        plot = go.Figure(
            data=[
                go.Bar(
                    name=givenEmailID1,
                    x=df1["Date"],
                    y=df1[testCaseType],
                ),
                go.Bar(
                    name=givenEmailID2,
                    x=df2["Date"],
                    y=df2[testCaseType],
                ),
            ]
        )
        plot.update_xaxes(
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
        if df1.shape[0] > 1 or df2.shape[0] > 1:
            plot.update_xaxes(
                range=[
                    start_date_object,
                    min(end_date_object, start_date_plus_twomonths),
                ]
            )
        plot.update_layout(
            height=900, width=1100, title="Developer Comparison (" + testCaseType + ")"
        )
        return plot
