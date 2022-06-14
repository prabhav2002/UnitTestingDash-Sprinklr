# importing libraries
from elasticsearch import Elasticsearch
from datetime import datetime as dt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
from dateutil.relativedelta import relativedelta
from homepage import homepage_row0

# connecting with elasticsearch server
es = Elasticsearch()

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


# function to get team-name of developer, get total testcases added, deleted, effective during select date-range
def devpage_row2(givenEmailID, startdate, enddate):
    if givenEmailID == None:
        return "Enter the Sprinklr Mail ID above to see the team...", 0, 0, 0
    else:
        # query to get date-wise aggregated count for testcases added, deleted, effective for selected developer
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
                "date": {
                    "date_histogram": {
                        "field": "fromTime",
                        "interval": "day",
                        "format": "yyyy-MM-dd",
                    },
                    "aggs": {
                        "DevwiseEffective": {"sum": {"field": "effectiveCount"}},
                        "DevwiseAdded": {"sum": {"field": "testAdded"}},
                        "DevwiseDeleted": {"sum": {"field": "testDeleted"}},
                    },
                }
            },
        }
        res = es.search(index="unit_test_tracker", body=query)
        data = []

        for i in res["aggregations"]["date"]["buckets"]:
            test_case_added = i["DevwiseAdded"]["value"]
            test_case_deleted = i["DevwiseDeleted"]["value"]
            effective_count = i["DevwiseEffective"]["value"]
            # converting timezone to Asia/Kolkata
            timestamp = i["key"] + 66600000
            date_time = dt.fromtimestamp(int(timestamp) / 1000)
            data.append(
                [date_time, effective_count, test_case_added, test_case_deleted]
            )

        # creating dataframe
        df = pd.DataFrame(
            data,
            columns=[
                "Date",
                "Effective Test Cases",
                "Test Cases Added",
                "Test Cases Deleted",
            ],
        )

        # filtering dataframe as per the date range chosen for analytics
        start_date_object = date.fromisoformat(startdate)
        start_date_string = start_date_object.strftime("%Y-%m-%d")
        end_date_object = date.fromisoformat(enddate)
        end_date_string = end_date_object.strftime("%Y-%m-%d")
        df = df[(df["Date"] >= start_date_string) & (df["Date"] <= end_date_string)]

        effectiveTestCases = df["Effective Test Cases"].sum()
        testCasesAdded = df["Test Cases Added"].sum()
        testCasesDeleted = df["Test Cases Deleted"].sum()

        # filter to get team-name of selected developer
        filter = {
            "size": 0,
            "query": {
                "term": {
                    "email.keyword": {
                        "value": givenEmailID,
                    }
                }
            },
            "aggs": {
                "team": {
                    "terms": {
                        "field": "cloudName.keyword",
                    }
                }
            },
        }
        result = es.search(index="unit_test_tracker", body=filter)
        teamNameSet = set()

        for i in result["aggregations"]["team"]["buckets"]:
            teamName = i["key"]
            teamNameSet.add(teamName)

        return str(teamNameSet), effectiveTestCases, testCasesAdded, testCasesDeleted


# function plot count of testcases vs time for selected developer for selected date-range
# selection for date-wise, week-wise, month-wise aggregation
# selection for type of testcases: added, deleted, effective
def devpage_row3(timePeriod, testCaseType, givenEmailID, startdate, enddate):
    if givenEmailID == None:
        return px.bar()
    else:
        # setting testcase-type
        if testCaseType == "Effective Test Cases":
            caseTypeString = "effectiveCount"
        elif testCaseType == "Test Cases Added":
            caseTypeString = "testAdded"
        elif testCaseType == "Test Cases Deleted":
            caseTypeString = "testDeleted"

        # query to get count selected testcase type date-wise aggregated for selected developer
        query_filter = {
            "size": 0,
            "query": {
                "term": {
                    "email.keyword": {
                        "value": givenEmailID,
                    }
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
        data = []
        for i in res["aggregations"]["date"]["buckets"]:
            testCaseCount = i["Total"]["value"]
            # converting timezone to Asia/Kolkata
            timestamp = i["key"] + 66600000
            date_time = dt.fromtimestamp(int(timestamp) / 1000)
            data.append([date_time, testCaseCount])

        # creating dataframe
        df = pd.DataFrame(data, columns=["Date", "TestCaseCount"])

        # filtering dataframe as per the date range chosen for analytics
        start_date_object = date.fromisoformat(startdate)
        start_date_string = start_date_object.strftime("%Y-%m-%d")
        end_date_object = date.fromisoformat(enddate)
        end_date_string = end_date_object.strftime("%Y-%m-%d")
        start_date_plus_fourmonths = start_date_object + relativedelta(months=4)
        df = df[(df["Date"] >= start_date_string) & (df["Date"] <= end_date_string)]

        # aggregated date-wise and plotting of data
        if timePeriod == "Date-wise Aggregation":
            fig = px.bar(
                df,
                x="Date",
                y="TestCaseCount",
                title=testCaseType + " by " + givenEmailID + " (Date-wise Aggregation)",
                height=900,
                width=1100,
            )
            fig.update_xaxes(
                rangeslider_visible=True,
                range=[
                    start_date_object,
                    min(start_date_plus_fourmonths, end_date_object),
                ],
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
            fig.update_yaxes(title=testCaseType)
            return fig

        # aggregated week-wise and plotting of data
        elif timePeriod == "Week-wise Aggregation":
            dfWeek = df.copy()
            dfWeek = (
                dfWeek.groupby([pd.Grouper(key="Date", freq="W-SUN")])[
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
                title=testCaseType + " by " + givenEmailID + " (Week-wise Aggregation)",
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
                dfMonth.groupby([pd.Grouper(key="Date", freq="1M")])[("TestCaseCount")]
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
                title=testCaseType
                + " by "
                + givenEmailID
                + " (Month-wise Aggregation)",
                height=900,
                width=1100,
            )
            fig.update_xaxes(title="Month", rangeslider_visible=True)
            fig.update_yaxes(title=testCaseType)
            return fig


# function to plot comparison between two developers for given date-range
# selection for testcase type: added, deleted, effective
def devpage_row4(givenEmailID1, givenEmailID2, testCaseType, startdate, enddate):
    if givenEmailID1 == None:
        return px.bar()
    elif givenEmailID2 == None:
        return px.bar()
    else:
        # setting testcase-type
        if testCaseType == "Effective Test Cases":
            caseTypeString = "effectiveCount"
        elif testCaseType == "Test Cases Added":
            caseTypeString = "testAdded"
        elif testCaseType == "Test Cases Deleted":
            caseTypeString = "testDeleted"

        # query to get count of given testcase type aggregated date-wise for first selected developer
        query_filter = {
            "size": 0,
            "query": {
                "term": {
                    "email.keyword": {
                        "value": givenEmailID1,
                    }
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
            timestamp = i["key"] + 66600000
            date_time = dt.fromtimestamp(int(timestamp) / 1000)
            data1.append([date_time, testCaseCount])

        # query to get count of given testcase type aggregated date-wise for selected selected developer
        query_filter = {
            "size": 0,
            "query": {
                "term": {
                    "email.keyword": {
                        "value": givenEmailID2,
                    }
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
            timestamp = i["key"] + 66600000
            date_time = dt.fromtimestamp(int(timestamp) / 1000)
            data2.append([date_time, testCaseCount])

        # creating two dataframes from the data we got
        df1 = pd.DataFrame(data1, columns=["Date", testCaseType])
        df2 = pd.DataFrame(data2, columns=["Date", testCaseType])

        # filtering dataframe as per the date range chosen for analytics
        start_date_object = date.fromisoformat(startdate)
        start_date_string = start_date_object.strftime("%Y-%m-%d")
        end_date_object = date.fromisoformat(enddate)
        end_date_string = end_date_object.strftime("%Y-%m-%d")
        start_date_plus_twomonths = start_date_object + relativedelta(months=2)

        df1 = df1[(df1["Date"] >= start_date_string) & (df1["Date"] <= end_date_string)]
        df2 = df2[(df2["Date"] >= start_date_string) & (df2["Date"] <= end_date_string)]

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
            range=[start_date_object, min(start_date_plus_twomonths, end_date_object)],
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
        plot.update_layout(
            height=900, width=1100, title="Developer Comparison (" + testCaseType + ")"
        )
        return plot