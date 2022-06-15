# importing libraries
from elasticsearch import Elasticsearch
from datetime import date
import pandas as pd

# connecting with elasticsearch server
es = Elasticsearch()

# create the leaderboard for the developers of the selected teams
def leaderboard_row1(teamNamesMultiDropdown, startdate, enddate):

    if type(teamNamesMultiDropdown) == str:
        teamNamesMultiDropdown = [teamNamesMultiDropdown]

    # converting startdate, enddate to timestamp
    start_date_object = date.fromisoformat(startdate)
    end_date_object = date.fromisoformat(enddate)

    data = []
    # query to get count of given testcase type developer wise for selected teams
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
            # aggregation to find count of every type of test cases of every developer of the team
            "aggs": {
                "dev": {
                    "terms": {"field": "email.keyword", "size": 2147483647},
                    "aggs": {
                        "TeamwiseEffective": {"sum": {"field": "effectiveCount"}},
                        "TeamwiseAdded": {"sum": {"field": "testAdded"}},
                        "TeamwiseDeleted": {"sum": {"field": "testDeleted"}},
                    },
                },
            },
        }
        res = es.search(index="unit_test_tracker", body=query_filter)

        # saving result to data
        for j in res["aggregations"]["dev"]["buckets"]:
            teamName = i
            devName = j["key"]
            effective_count = j["TeamwiseEffective"]["value"]
            test_added = j["TeamwiseAdded"]["value"]
            test_deleted = j["TeamwiseDeleted"]["value"]
            data.append([devName, teamName, effective_count, test_added, test_deleted])
        # creating dataframe
        df = pd.DataFrame(
            data,
            columns=[
                "Email",
                "Team",
                "Effective Test Cases",
                "Test Cases Added",
                "Test Cases Deleted",
            ],
        )
    return df
