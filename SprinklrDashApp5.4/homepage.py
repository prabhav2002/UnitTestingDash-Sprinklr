from elasticsearch import Elasticsearch
from datetime import datetime as dt
import pandas as pd
import plotly.express as px
from datetime import date
from dateutil.relativedelta import relativedelta

es = Elasticsearch()

def homepage_row0():
    query_filter={
        "size": 0,
        "aggs": {"date": {"date_histogram":{  
            "field":"fromTime",
            "interval":"day",
            "format" : "yyyy-MM-dd"
     }}}
    }
    res = es.search( index = "unit_test_tracker", body = query_filter)

    min_date = 0
    max_date = 0
    data=[]

    for i in res["aggregations"]["date"]["buckets"]:
        timestamp = i["key"]+66600000
        date_time = dt.fromtimestamp(int(timestamp)/1000)
        data.append([date_time])
    df = pd.DataFrame(data, columns = ['Date'])

    column = df['Date']
    max_date = column.max()
    column = df['Date']
    min_date = column.min()

    return min_date, max_date

def homepage_row1():
    query_filter={
        "size": 0,
        "aggs": {
            "total_added" : {
                "sum" : { "field" : "testAdded" }
            },
            "total_deleted" : {
                "sum" : { "field" : "testDeleted" }
            },
            "total_effective" : {
                "sum" : { "field" : "effectiveCount" }
            }
        }   
    }
    result = es.search( index = "unit_test_tracker", body = query_filter)
    totalAdded = result['aggregations']['total_added']['value']
    totalDeleted = result['aggregations']['total_deleted']['value']
    totalEffective = result['aggregations']['total_effective']['value']
    return (totalAdded, totalDeleted, totalEffective)

def homepage_row2():
    query_filter={
        "size": 0,
        "aggs": {
            "team":{"terms": {"field": "cloudName.keyword", "size": 2147483647}},
            "dev":{"terms": {"field": "email.keyword", "size": 2147483647}}
        }
    }
    result = es.search( index = "unit_test_tracker", body = query_filter)
    teamSet = set()
    devSet = set()
    for i in result["aggregations"]["dev"]["buckets"]:
        dev = i["key"]
        devSet.add(dev)
    for i in result["aggregations"]["team"]["buckets"]:
        team = i["key"]
        teamSet.add(team)
        
    return len(devSet), len(teamSet)

def homepage_row3(timePeriod, startdate, enddate):
    query_filter={
        "size": 0,
        "aggs": {
            "date": {
                "date_histogram":{  
                    "field":"fromTime",
                    "interval":"day",
                    "format" : "yyyy-MM-dd"
            },
            "aggs":{
                "DatewiseEffective": {"sum": {"field": "effectiveCount"}},
                "DatewiseAdded": {"sum": {"field": "testAdded"}},
                "DatewiseDeleted": {"sum": {"field": "testDeleted"}}
            }}
        }}
    res = es.search(index="unit_test_tracker", body=query_filter)
    data=[]
    for i in res["aggregations"]["date"]["buckets"]:
        effective_count = i["DatewiseEffective"]["value"]
        test_added = i["DatewiseAdded"]["value"]
        test_deleted = i["DatewiseDeleted"]["value"]
        timestamp = i["key"]+66600000
        date_time = dt.fromtimestamp(int(timestamp)/1000)
        data.append([date_time, effective_count, test_added, test_deleted])
    
    df = pd.DataFrame(data, columns = ['Date', 'TotalEffectiveTests', 'TotalTestsAdded', 'TotalTestsDeleted'])

    start_date_object = date.fromisoformat(startdate)
    start_date_string = start_date_object.strftime('%Y-%m-%d')
    end_date_object = date.fromisoformat(enddate)
    end_date_string = end_date_object.strftime('%Y-%m-%d')
    start_date_plus_month = start_date_object + relativedelta(months=1)
    df = df[(df['Date'] >= start_date_string) & (df['Date'] <= end_date_string)]

    if timePeriod == "Week-wise Aggregation":
        dfWeek = df.copy()
        dfWeek = dfWeek.groupby([pd.Grouper(key='Date', freq='W-SUN')])[('TotalEffectiveTests', 'TotalTestsAdded', 'TotalTestsDeleted')].sum().reset_index().sort_values('Date')
        dfWeek['Date'] = dfWeek['Date'].dt.strftime("%W")
        plot = px.bar(dfWeek, x='Date', y=df.columns, title="Week-wise Unit Testing Aggregation", labels={'Date': 'Week'}, height=700)
        plot.update_xaxes(title = "Week Number of the Year",rangeslider_visible=True) 
        plot.update_yaxes(title="Test Cases Count")
        plot.update_layout(legend=dict(title='<b>Click here to<br>activate/deactivate<br>specific Test Case<br>Count Type<b>'))
        return plot
    elif timePeriod == "Month-wise Aggregation":
        dfMonth = df.copy()
        dfMonth = dfMonth.groupby([pd.Grouper(key='Date', freq='1M')])[('TotalEffectiveTests', 'TotalTestsAdded', 'TotalTestsDeleted')].sum().reset_index().sort_values('Date')
        dfMonth['Date'] = dfMonth['Date'].dt.strftime("%B")
        plot = px.bar(dfMonth, x='Date', y=df.columns, title="Month-wise Unit Testing Aggregation", labels={'Date': 'Month'}, height=700)
        plot.update_xaxes(title = "Months", rangeslider_visible=True) 
        plot.update_yaxes(title="Test Cases Count")
        plot.update_layout(legend=dict(title='<b>Click here to<br>activate/deactivate<br>specific Test Case<br>Count Type<b>'))
        return plot
    else:
        plot = px.bar(df, x="Date", y=df.columns, title="Date-wise Unit Testing Aggregation", height=700)   
        plot.update_xaxes(
            rangeslider_visible=True,
            range=[start_date_object, min(start_date_plus_month, end_date_object)],
            rangeselector=dict(
                buttons=list([
                    dict(count=7, label="1w", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(step="all")
                ])
            )
        ) 
        plot.update_yaxes(title="Test Cases Count")
        plot.update_layout(legend=dict(title='<b>Click here to<br>activate/deactivate<br>specific Test Case<br>Count Type<b>'))
        return plot