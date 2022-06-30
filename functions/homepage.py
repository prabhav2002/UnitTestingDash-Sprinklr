# importing libraries
from functions.elasticServerDashApp import elasitcServerDashApp
from datetime import datetime as dt
import pandas as pd
import plotly.express as px
from datetime import date
import plotly.graph_objects as go
from dateutil.relativedelta import relativedelta

# function to get minimum and maximum date of the available data
def homepage_row0():
    # connecting with elasticsearch server
    es = elasitcServerDashApp()
    # taking minimum and maximum from "fromTime" column consisting of timestamp as aggregation
    query_filter = {
        "size": 0,
        "aggs": {
            "min_date": {"min": {"field": "fromTime", "format": "yyyy-MM-dd"}},
            "max_date": {"max": {"field": "fromTime", "format": "yyyy-MM-dd"}},
        },
    }
    res = es.search(index="unit_test_tracker", body=query_filter)

    # getting min_date and max_date from resultant timestamp, addition of +86400000 to change the timezone
    min_date = dt.fromtimestamp(
        (int(res["aggregations"]["min_date"]["value"]) + 86400000) / 1000
    )
    max_date = dt.fromtimestamp(
        (int(res["aggregations"]["max_date"]["value"]) + 86400000) / 1000
    )
    return min_date, max_date


# function to get total testcases added, total testcases deleted and total effective testcases in the given date range
def homepage_row1(startdate, enddate):
    # connecting with elasticsearch server
    es = elasitcServerDashApp()
    # converting startdate, enddate to timestamp
    start_date_object = date.fromisoformat(startdate)
    end_date_object = date.fromisoformat(enddate)

    # counting overall testCasesAdded, testCasesDeleted, and totalEffectivetestCases by aggregation in the selected date range
    query_filter = {
        "size": 0,
        "query": {
            "range": {
                "fromTime": {
                    "time_zone": "+05:30",
                    "gte": start_date_object,
                    "lte": end_date_object,
                }
            }
        },
        "aggs": {
            "total_added": {"sum": {"field": "testAdded"}},
            "total_deleted": {"sum": {"field": "testDeleted"}},
            "total_effective": {"sum": {"field": "effectiveCount"}},
        },
    }
    result = es.search(index="unit_test_tracker", body=query_filter)

    totalAdded = result["aggregations"]["total_added"]["value"]
    totalDeleted = result["aggregations"]["total_deleted"]["value"]
    totalEffective = result["aggregations"]["total_effective"]["value"]

    return (totalAdded, totalDeleted, totalEffective)


# function to get count of unique teams and unique developers in the provided data
def homepage_row2():
    # connecting with elasticsearch server
    es = elasitcServerDashApp()
    # counting distinct number of teams and devs using cardinality as aggregation method
    query_filter = {
        "size": 0,
        "aggs": {
            "team": {"cardinality": {"field": "cloudName.keyword"}},
            "dev": {"cardinality": {"field": "email.keyword"}},
        },
    }
    result = es.search(index="unit_test_tracker", body=query_filter)

    numberOfTeams = result["aggregations"]["team"]["value"]
    numberOfDevs = result["aggregations"]["dev"]["value"]

    return numberOfDevs, numberOfTeams


# function to plot overall data analytics
# and get dataframe of overall analytics
# with the feature of date-wise, week-wise, month-wise aggregation
def homepage_row3(timePeriod, startdate, enddate):
    # connecting with elasticsearch server
    es = elasitcServerDashApp()
    # converting startdate, enddate to timestamp
    start_date_object = date.fromisoformat(startdate)
    end_date_object = date.fromisoformat(enddate)

    # query to get the aggregation date-wise with total count of testcases added, deleted and effective in the selected date range.
    query_filter = {
        "size": 0,
        # putting start-date and end-date range as filter
        "query": {
            "range": {
                "fromTime": {
                    "time_zone": "+05:30",
                    "gte": start_date_object,
                    "lte": end_date_object,
                }
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

    # saving result to the data
    data = []
    for i in res["aggregations"]["date"]["buckets"]:
        effective_count = i["DatewiseEffective"]["value"]
        test_added = i["DatewiseAdded"]["value"]
        test_deleted = i["DatewiseDeleted"]["value"]
        # converting timezone to Asia/Kolkata
        timestamp = i["key"] + 86400000
        date_time = dt.fromtimestamp(int(timestamp) / 1000)
        data.append([date_time, effective_count, test_added, test_deleted])

    if len(data) == 0:
        dataNone = []
        dfNone = pd.DataFrame(dataNone, columns=["No Data"])
        plot = go.Figure()
        plot.update_layout(
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
        return plot, dfNone

    # creating dataframe
    dfHome = pd.DataFrame(
        data,
        columns=[
            "Date",
            "Effective Test Cases",
            "Test Cases Added",
            "Test Cases Deleted",
        ],
    )

    # plotting daily stats
    if timePeriod == "Daily":
        plot = px.bar(
            dfHome,
            x="Date",
            y=dfHome.columns,
            color_discrete_sequence=["#636EFA", "#00CC96", "#EF553B"],
            title="Unit Testing Analytics (Daily)",
            height=700,
        )
        dfHome["Date"] = dfHome["Date"].dt.strftime("%Y-%m-%d")
        start_date_plus_month = start_date_object + relativedelta(months=1)
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
        plot.update_yaxes(title="Test Cases Count")
        if dfHome.shape[0] > 1:
            plot.update_xaxes(
                range=[start_date_object, min(start_date_plus_month, end_date_object)],
            )
        plot.update_layout(
            legend=dict(
                title="<b>Click here to<br>activate/deactivate<br>specific Test Case<br>Count Type<b>"
            )
        )
        return plot, dfHome

    # converting dataframe for weekly stats and plotting of dataframe
    elif timePeriod == "Weekly":
        dfWeek = dfHome.copy()
        dfWeek = (
            dfWeek.groupby([pd.Grouper(key="Date", freq="W-SUN")])[
                ["Effective Test Cases", "Test Cases Added", "Test Cases Deleted"]
            ]
            .sum()
            .reset_index()
            .sort_values("Date")
        )
        dfWeek["Date"] = dfWeek["Date"] - pd.to_timedelta(6, unit="d")
        dfWeek["Date"] = dfWeek["Date"].dt.strftime("%Y-%m-%d")
        plot = px.bar(
            dfWeek,
            x="Date",
            y=dfWeek.columns,
            labels={"Date": "Start Date of the Week"},
            title="Unit Testing Analytics (Weekly)",
            height=700,
        )
        plot.update_xaxes(title="Start Date of the Week", rangeslider_visible=True)
        plot.update_yaxes(title="Test Cases Count")
        plot.update_layout(
            legend=dict(
                title="<b>Click here to<br>activate/deactivate<br>specific Test Case<br>Count Type<b>"
            )
        )
        dfWeek.rename(columns={"Date": "Start Date of the Week"}, inplace=True)
        return plot, dfWeek

    # converting dataframe for monthly stats and plotting of dataframe
    elif timePeriod == "Monthly":
        dfMonth = dfHome.copy()
        dfMonth = (
            dfMonth.groupby([pd.Grouper(key="Date", freq="1M")])[
                ["Effective Test Cases", "Test Cases Added", "Test Cases Deleted"]
            ]
            .sum()
            .reset_index()
            .sort_values("Date")
        )
        dfMonth["Date"] = dfMonth["Date"].dt.strftime("%Y, %m (%b)")
        plot = px.bar(
            dfMonth,
            x="Date",
            y=dfMonth.columns,
            title="Unit Testing Analytics (Monthly)",
            labels={"Date": "Month"},
            height=700,
        )
        plot.update_xaxes(title="Months", rangeslider_visible=True)
        plot.update_yaxes(title="Test Cases Count")
        plot.update_layout(
            legend=dict(
                title="<b>Click here to<br>activate/deactivate<br>specific Test Case<br>Count Type<b>"
            )
        )
        dfMonth.rename(columns={"Date": "Month"}, inplace=True)
        return plot, dfMonth
