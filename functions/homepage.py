# importing libraries
from elasticServerDashApp import elasitcServerDashApp
from datetime import datetime as dt
import pandas as pd
import plotly.express as px
from datetime import date
import plotly.graph_objects as go
from dateutil.relativedelta import relativedelta

# connecting with elasticsearch server
es = elasitcServerDashApp()

# function to get minimum and maximum date of the available data
def homepage_row0():
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
# and get JSONfied dataframe of overall analytics
# with the feature of date-wise, week-wise, month-wise aggregation
def homepage_row3(timePeriod, startdate, enddate):

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

    # creating dataframe
    df = pd.DataFrame(
        data,
        columns=["Date", "TotalEffectiveTests", "TotalTestsAdded", "TotalTestsDeleted"],
    )

    if df.shape[0] == 0:
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

    # converting dataframe for weekly stats and plotting of dataframe
    if timePeriod == "Weekly":
        dfWeek = df.copy()
        dfWeek = (
            dfWeek.groupby([pd.Grouper(key="Date", freq="W-SUN")])[
                ["TotalEffectiveTests", "TotalTestsAdded", "TotalTestsDeleted"]
            ]
            .sum()
            .reset_index()
            .sort_values("Date")
        )
        dfWeek["Date"] = dfWeek["Date"].dt.strftime("%W, %Y")
        plot = px.bar(
            dfWeek,
            x="Date",
            y=df.columns,
            labels={"Date": "Week Number of the Year"},
            title="Unit Testing Analytics (Weekly)",
            height=700,
        )
        plot.update_xaxes(title="Week Number of the Year", rangeslider_visible=True)
        plot.update_yaxes(title="Test Cases Count")
        plot.update_layout(
            legend=dict(
                title="<b>Click here to<br>activate/deactivate<br>specific Test Case<br>Count Type<b>"
            )
        )
        dfWeek.rename(columns={"Date": "Week Number of the Year"}, inplace=True)
        return plot, dfWeek.to_json(orient="split")

    # converting dataframe for monthly stats and plotting of dataframe
    elif timePeriod == "Monthly":
        dfMonth = df.copy()
        dfMonth = (
            dfMonth.groupby([pd.Grouper(key="Date", freq="1M")])[
                ["TotalEffectiveTests", "TotalTestsAdded", "TotalTestsDeleted"]
            ]
            .sum()
            .reset_index()
            .sort_values("Date")
        )
        dfMonth["Date"] = dfMonth["Date"].dt.strftime("%b, %Y")
        plot = px.bar(
            dfMonth,
            x="Date",
            y=df.columns,
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
        return plot, dfMonth.to_json(orient="split")

    # plotting daily stats
    else:
        plot = px.bar(
            df,
            x="Date",
            y=df.columns,
            title="Unit Testing Analytics (Daily)",
            height=700,
        )
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
        if df.shape[0] > 1:
            plot.update_xaxes(
                range=[start_date_object, min(start_date_plus_month, end_date_object)],
            )
        plot.update_layout(
            legend=dict(
                title="<b>Click here to<br>activate/deactivate<br>specific Test Case<br>Count Type<b>"
            )
        )
        return plot, df.to_json(orient="split")
