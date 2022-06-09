from elasticsearch import Elasticsearch
from datetime import datetime as dt
from datetime import date
import pandas as pd
import plotly.express as px
from dateutil.relativedelta import relativedelta

es = Elasticsearch()

def teampage_row1():
    query_filter={
        "size": 0,
        "aggs": {
            "team":{"terms": {"field": "cloudName.keyword", "size": 2147483647}},
        }
    }
    result = es.search( index = "unit_test_tracker", body = query_filter)
    teamSet = set()
    for i in result["aggregations"]["team"]["buckets"]:
        team = i["key"]
        teamSet.add(team)
    teamList = []
    teamList = list(teamSet)
    teamList.sort()
    return len(teamSet), teamList

def teampage_row2():
    teams, teamList = teampage_row1()
    data = []
    for i in teamList:
        query_filter={
        "from":0,
        "size":10000,
        "query": {
            "term": {
                "cloudName.keyword": {
                    "value": i,
                }
            }
        },
        "aggs": {
            "dev":{"terms": {"field": "email.keyword", "size": 2147483647}}
        }}
        res = es.search(index="unit_test_tracker", body=query_filter)
        for j in res["aggregations"]["dev"]["buckets"]:
            devName = j["key"]
            data.append([i,devName])

    df = pd.DataFrame(data, columns = ['Team', 'Email'])
    teamList.sort()
    chartData = []
    for i in teamList:
        teamNameForChart = i
        devCountPerTeamForChart = df['Team'].value_counts()[i]
        chartData.append([teamNameForChart, devCountPerTeamForChart])
    dfChart = pd.DataFrame(chartData, columns = ['teamName', 'devCountPerTeam'])
    dfChart = dfChart.sort_values(by = 'teamName')
    fig = px.pie(dfChart, values='devCountPerTeam', names='teamName', hole=.3, title='<b>Number of Developers per Team<b>')
    return fig

def teampage_row3(timePeriod, teamNamesMultiDropdown, testCaseType, startdate, enddate):
    if type(teamNamesMultiDropdown) == str:
        teamNamesMultiDropdown = [teamNamesMultiDropdown]

    if testCaseType == "Effective Test Cases":
        caseTypeString = "effectiveCount"
    elif testCaseType == "Test Cases Added": 
        caseTypeString = "testAdded"
    elif testCaseType == "Test Cases Deleted":
        caseTypeString = "testDeleted"
    data = []
    for i in teamNamesMultiDropdown:
        query_filter={
            "from":0,
            "size":10000,
            "query": {
                "term": {
                    "cloudName.keyword": {
                        "value": i,
                    }
                }
            },
            "aggs": {
                "date": {
                    "date_histogram":{  
                        "field":"fromTime",
                        "interval":"day",
                        "format" : "yyyy-MM-dd"
                },
                "aggs":{"Total": {"sum": {"field": caseTypeString}}}
                }
            }}
        res = es.search(index="unit_test_tracker", body=query_filter)
        for j in res["aggregations"]["date"]["buckets"]:
            teamName = i
            testCaseCount = j["Total"]["value"]
            timestamp = j["key"]+66600000
            date_time = dt.fromtimestamp(int(timestamp)/1000)
            data.append([date_time, testCaseCount, teamName])

    df = pd.DataFrame(data, columns = ['Date', 'TestCaseCount', 'Team'])  

    start_date_object = date.fromisoformat(startdate)
    start_date_string = start_date_object.strftime('%Y-%m-%d')
    end_date_object = date.fromisoformat(enddate)
    end_date_string = end_date_object.strftime('%Y-%m-%d')

    df = df[(df['Date'] >= start_date_string) & (df['Date'] <= end_date_string)]
    start_date_plus_month = start_date_object + relativedelta(months=1) 

    if timePeriod == "Date-wise Aggregation":
        fig = px.bar(df, x='Date', y='TestCaseCount', color='Team', title='Team-wise '+ testCaseType, height=900, width=1100)
        fig.update_xaxes(
            rangeslider_visible=True,
            range=[start_date_object, min(start_date_plus_month,end_date_object)],
            rangeselector=dict(
                buttons=list([
                    dict(count=7, label="1w", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )
        fig.update_yaxes(title=testCaseType)
        return fig
    elif timePeriod == "Week-wise Aggregation":
        dfWeek = df.copy()
        dfWeek = dfWeek.groupby(['Team', pd.Grouper(key='Date', freq='W-SUN')])[('TestCaseCount')].sum().reset_index().sort_values('Date')
        dfWeek['Date'] = dfWeek['Date'].dt.strftime("%W")
        dfWeek.rename(columns = {'Date':'Week'}, inplace = True)
        fig = px.bar(dfWeek, x='Week', y='TestCaseCount', color='Team', title='Team-wise '+ testCaseType, height=900, width=1100)
        fig.update_xaxes(title = "Week Number of the Year",rangeslider_visible=True)
        fig.update_yaxes(title=testCaseType)
        return fig
    else:
        dfMonth = df.copy()
        dfMonth = dfMonth.groupby(['Team', pd.Grouper(key='Date', freq='1M')])[('TestCaseCount')].sum().reset_index().sort_values('Date')
        dfMonth['Date'] = dfMonth['Date'].dt.strftime("%B")
        dfMonth.rename(columns = {'Date':'Month'}, inplace = True)
        fig = px.bar(dfMonth, x='Month', y='TestCaseCount', color='Team', title='Team-wise '+ testCaseType, height=900, width=1100)
        fig.update_xaxes(title = "Month",rangeslider_visible=True)
        fig.update_yaxes(title=testCaseType)
        return fig

def teampage_row4(team, testCaseType):
    if testCaseType == "Effective Test Cases":
        caseTypeString = "effectiveCount"
    elif testCaseType == "Test Cases Added": 
        caseTypeString = "testAdded"
    elif testCaseType == "Test Cases Deleted":
        caseTypeString = "testDeleted"
    teams, teamList = teampage_row1()
    data = []
    for i in teamList:
        query_filter={
        "from":0,
        "size":0,
        "query": {
            "term": {
                "cloudName.keyword": {
                    "value": i,
                }
            }
        },
        "aggs": {
            "dev":{"terms": {"field": "email.keyword", "size": 2147483647},
            "aggs": {"testCaseCount": {"sum": {"field": caseTypeString}}},},
        }}
        res = es.search(index="unit_test_tracker", body=query_filter)
        for j in res["aggregations"]["dev"]["buckets"]:
            devName = j["key"]
            count = j["testCaseCount"]["value"]
            data.append([i,devName,count])
    
    df = pd.DataFrame(data, columns = ['Team', 'Email', 'Test Case Count'])
    teamList.sort()
    dfListTeamwise = {}
    for i in teamList:
        dfListTeamwise[i] = (df[(df['Team'] == str(i))])
        dfListTeamwise[i] = dfListTeamwise[i].sort_values('Email')
    fig = px.bar(dfListTeamwise[team], x='Email', y='Test Case Count', title='Total '+testCaseType+' by Developers (Team: '+team+' )', height=900, width=1100)
    return fig