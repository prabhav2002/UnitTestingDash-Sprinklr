# importing libraries
from elasticsearch import Elasticsearch
from datetime import datetime as dt
from datetime import date
import pandas as pd

# connecting with elasticsearch server
es = Elasticsearch()

# function to JSONfied dataframe of overall analytics for the  given DateRange
def exportpage_row1(timePeriod, startdate, enddate):

    # converting startdate, enddate to timestamp
    start_date_object = date.fromisoformat(startdate)
    end_date_object = date.fromisoformat(enddate)

    query_filter = {
        "size": 0,
        "query": {
            # filter to get the results of selected date range only
            "range": {
                "fromTime": {
                    "time_zone": "+05:30",
                    "gte": start_date_object,
                    "lte": end_date_object,
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
        timestamp = i["key"] + 66600000
        date_time = dt.fromtimestamp(int(timestamp) / 1000)
        data.append([date_time, effective_count, test_added, test_deleted])

    df = pd.DataFrame(
        data,
        columns=["Date", "TotalEffectiveTests", "TotalTestsAdded", "TotalTestsDeleted"],
    )

    if timePeriod == "Week-wise Aggregation":
        dfWeek = df.copy()
        dfWeek = (
            dfWeek.groupby([pd.Grouper(key="Date", freq="W-SUN")])[
                ("TotalEffectiveTests", "TotalTestsAdded", "TotalTestsDeleted")
            ]
            .sum()
            .reset_index()
            .sort_values("Date")
        )
        dfWeek["Date"] = dfWeek["Date"].dt.strftime("%W")
        dfWeek.rename(columns={"Date": "Week Number of the Year"}, inplace=True)
        return dfWeek.to_json(orient="split")
    elif timePeriod == "Month-wise Aggregation":
        dfMonth = df.copy()
        dfMonth = (
            dfMonth.groupby([pd.Grouper(key="Date", freq="1M")])[
                ("TotalEffectiveTests", "TotalTestsAdded", "TotalTestsDeleted")
            ]
            .sum()
            .reset_index()
            .sort_values("Date")
        )
        dfMonth["Date"] = dfMonth["Date"].dt.strftime("%B")
        dfMonth.rename(columns={"Date": "Month"}, inplace=True)
        return dfMonth.to_json(orient="split")
    else:
        return df.to_json(orient="split")


# function to JSONfied dataframe of developer-wise analytics for the  given DateRange
def exportpage_row2(givenEmailID, timePeriod, startdate, enddate):

    # converting startdate, enddate to timestamp
    start_date_object = date.fromisoformat(startdate)
    end_date_object = date.fromisoformat(enddate)

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
                    "DevwiseEffective": {"sum": {"field": "effectiveCount"}},
                    "DevwiseAdded": {"sum": {"field": "testAdded"}},
                    "DevwiseDeleted": {"sum": {"field": "testDeleted"}},
                },
            }
        },
    }
    res = es.search(index="unit_test_tracker", body=query_filter)

    data = []
    for i in res["aggregations"]["date"]["buckets"]:
        effective_count = i["DevwiseEffective"]["value"]
        test_added = i["DevwiseAdded"]["value"]
        test_deleted = i["DevwiseDeleted"]["value"]
        timestamp = i["key"] + 66600000
        date_time = dt.fromtimestamp(int(timestamp) / 1000)
        data.append([date_time, test_added, test_deleted, effective_count])
    df = pd.DataFrame(
        data, columns=["Date", "Test Added", "Test Deleted", "Effective Test Cases"]
    )

    if timePeriod == "Date-wise Aggregation":
        return df.to_json(orient="split")
    elif timePeriod == "Week-wise Aggregation":
        dfWeek = df.copy()
        dfWeek = (
            dfWeek.groupby([pd.Grouper(key="Date", freq="W-SUN")])[
                ("Test Added", "Test Deleted", "Effective Test Cases")
            ]
            .sum()
            .reset_index()
            .sort_values("Date")
        )
        dfWeek["Date"] = dfWeek["Date"].dt.strftime("%W")
        dfWeek.rename(columns={"Date": "Week Number of the Year"}, inplace=True)
        return dfWeek.to_json(orient="split")
    else:
        dfMonth = df.copy()
        dfMonth = (
            dfMonth.groupby([pd.Grouper(key="Date", freq="1M")])[
                ("Test Added", "Test Deleted", "Effective Test Cases")
            ]
            .sum()
            .reset_index()
            .sort_values("Date")
        )
        dfMonth["Date"] = dfMonth["Date"].dt.strftime("%B")
        dfMonth.rename(columns={"Date": "Month"}, inplace=True)
        return dfMonth.to_json(orient="split")


# function to JSONfied dataframe of team-wise analytics for the  given DateRange
def exportpage_row3(givenTeam, timePeriod, startdate, enddate):

    # converting startdate, enddate to timestamp
    start_date_object = date.fromisoformat(startdate)
    end_date_object = date.fromisoformat(enddate)

    query_filter = {
        "size": 0,
        "query": {
            "bool": {
                "must": [
                    {"match": {"cloudName.keyword": givenTeam}},
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
                    "TeamwiseEffective": {"sum": {"field": "effectiveCount"}},
                    "TeamwiseAdded": {"sum": {"field": "testAdded"}},
                    "TeamwiseDeleted": {"sum": {"field": "testDeleted"}},
                },
            }
        },
    }
    res = es.search(index="unit_test_tracker", body=query_filter)

    data = []
    for i in res["aggregations"]["date"]["buckets"]:
        effective_count = i["TeamwiseEffective"]["value"]
        test_added = i["TeamwiseAdded"]["value"]
        test_deleted = i["TeamwiseDeleted"]["value"]
        timestamp = i["key"] + 66600000
        date_time = dt.fromtimestamp(int(timestamp) / 1000)
        data.append([date_time, test_added, test_deleted, effective_count])
    df = pd.DataFrame(
        data, columns=["Date", "Test Added", "Test Deleted", "Effective Test Cases"]
    )

    if timePeriod == "Date-wise Aggregation":
        return df.to_json(orient="split")
    elif timePeriod == "Week-wise Aggregation":
        dfWeek = df.copy()
        dfWeek = (
            dfWeek.groupby([pd.Grouper(key="Date", freq="W-SUN")])[
                ("Test Added", "Test Deleted", "Effective Test Cases")
            ]
            .sum()
            .reset_index()
            .sort_values("Date")
        )
        dfWeek["Date"] = dfWeek["Date"].dt.strftime("%W")
        dfWeek.rename(columns={"Date": "Week Number of the Year"}, inplace=True)
        return dfWeek.to_json(orient="split")
    else:
        dfMonth = df.copy()
        dfMonth = (
            dfMonth.groupby([pd.Grouper(key="Date", freq="1M")])[
                ("Test Added", "Test Deleted", "Effective Test Cases")
            ]
            .sum()
            .reset_index()
            .sort_values("Date")
        )
        dfMonth["Date"] = dfMonth["Date"].dt.strftime("%B")
        dfMonth.rename(columns={"Date": "Month"}, inplace=True)
        return dfMonth.to_json(orient="split")


# function to JSONfied dataframe of developer-wise test cases count for selected team
def exportpage_row4(givenTeam, startdate, enddate):

    # converting startdate, enddate to timestamp
    start_date_object = date.fromisoformat(startdate)
    end_date_object = date.fromisoformat(enddate)

    query_filter = {
        "size": 0,
        "query": {
            "bool": {
                "must": [
                    {"match": {"cloudName.keyword": givenTeam}},
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
            "dev": {
                "terms": {"field": "email.keyword", "size": 2147483647},
                "aggs": {
                    "TeamwiseEffective": {"sum": {"field": "effectiveCount"}},
                    "TeamwiseAdded": {"sum": {"field": "testAdded"}},
                    "TeamwiseDeleted": {"sum": {"field": "testDeleted"}},
                },
            }
        },
    }
    res = es.search(index="unit_test_tracker", body=query_filter)

    data = []
    for i in res["aggregations"]["dev"]["buckets"]:
        effective_count = i["TeamwiseEffective"]["value"]
        test_added = i["TeamwiseAdded"]["value"]
        test_deleted = i["TeamwiseDeleted"]["value"]
        devName = i["key"]
        data.append([devName, test_added, test_deleted, effective_count])
    df = pd.DataFrame(
        data,
        columns=["Developer", "Test Added", "Test Deleted", "Effective Test Cases"],
    )
    df = df.sort_values("Developer")
    return df.to_json(orient="split")
