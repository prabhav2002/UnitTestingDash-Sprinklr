# importing libraries
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import date
from datetime import datetime as dt
from exportpage import (
    exportpage_row1,
    exportpage_row2,
    exportpage_row3,
    exportpage_row4,
)
from devpage import devpage_row1
from teampage import teampage_row1
from homepage import homepage_row0
from app import app

# getting minimum and maximum date in provided data using homepage function
min_date, max_date = homepage_row0()
min_datem = dt.strptime(str(min_date), "%Y-%m-%d %H:%M:%S")
max_datem = dt.strptime(str(max_date), "%Y-%m-%d %H:%M:%S")

# getting list of all developers from the provided data
devEmailList = devpage_row1()
# getting list of all teams from the provided data
totalTeams, teamList = teampage_row1()

# layout of exports page
layout = html.Div(
    [
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.H1(
                                "Download the filtered data as Excel!",
                                className="text-center",
                            ),
                            className="mb-5 mt-5",
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.H3(
                                "Select a date range to get the stats of that specific time-period",
                                className="text-center",
                            ),
                            className="mb-5 mt-5",
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(dbc.Card(), className="mb-4"),
                        dbc.Col(
                            dbc.Card(
                                children=[
                                    dcc.DatePickerRange(
                                        id="exp-date-picker-range",
                                        min_date_allowed=date(
                                            min_datem.year,
                                            min_datem.month,
                                            min_datem.day,
                                        ),
                                        max_date_allowed=date(
                                            max_datem.year,
                                            max_datem.month,
                                            max_datem.day,
                                        ),
                                        display_format="DD-MM-YYYY",
                                        initial_visible_month=date(
                                            min_datem.year,
                                            min_datem.month,
                                            min_datem.day,
                                        ),
                                        start_date=date(
                                            min_datem.year,
                                            min_datem.month,
                                            min_datem.day,
                                        ),
                                        end_date=date(
                                            max_datem.year,
                                            max_datem.month,
                                            max_datem.day,
                                        ),
                                    )
                                ],
                                body=True,
                                color="primary",
                                outline=False,
                            ),
                            className="mb-4",
                        ),
                        dbc.Col(dbc.Card(), className="mb-4"),
                    ],
                    className="mb-5",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.H2(
                                children="Overall Analytics", className="text-center"
                            ),
                            className="mb-4",
                        )
                    ]
                ),
                dcc.Dropdown(
                    [
                        "Date-wise Aggregation",
                        "Week-wise Aggregation",
                        "Month-wise Aggregation",
                    ],
                    "Date-wise Aggregation",
                    clearable=False,
                    id="timePeriod-dropdown-exportpage1",
                ),
                dcc.Store(id="overall_analytics_df"),
                dbc.Row([]),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                children=[
                                    html.H4(
                                        children="Overall Analytics as per the above filter",
                                        className="text-center",
                                    ),
                                    dbc.Button(
                                        "Download as Excel",
                                        id="overall_button_xlsx",
                                        color="primary",
                                        className="mt-3",
                                    ),
                                ],
                                body=True,
                                color="dark",
                                outline=True,
                            ),
                            className="mb-4 mt-4",
                        ),
                    ]
                ),
                dcc.Download(id="overall_analytics_download_xlsx"),
                dbc.Row(
                    [
                        dbc.Col(
                            html.H2(
                                "Developer-wise Unit-Testing Analytics",
                                className="text-center",
                            ),
                            className="mb-4",
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.H5(
                                "Select a developer to see the stats",
                                className="text-center",
                            ),
                            className="mb-4",
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Dropdown(
                                devEmailList,
                                placeholder="Type Sprinklr Email ID of Developer...",
                                clearable=False,
                                id="devMail-dropdown-exportpage",
                            )
                        ),
                        dbc.Col(
                            dcc.Dropdown(
                                [
                                    "Date-wise Aggregation",
                                    "Week-wise Aggregation",
                                    "Month-wise Aggregation",
                                ],
                                "Date-wise Aggregation",
                                clearable=False,
                                id="timePeriod-dropdown-devexportpage",
                            )
                        ),
                    ],
                    className="mb-5",
                ),
                dcc.Store(id="dev_analytics_df"),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                children=[
                                    html.H4(
                                        children="Developer-wise Analytics as per the above filter",
                                        className="text-center",
                                    ),
                                    dbc.Button(
                                        "Download as Excel",
                                        id="dev_button_xlsx",
                                        color="primary",
                                        className="mt-3",
                                    ),
                                ],
                                body=True,
                                color="dark",
                                outline=True,
                            ),
                            className="mb-4",
                        ),
                    ]
                ),
                dcc.Download(id="dev_analytics_download_xlsx"),
                dbc.Row(
                    [
                        dbc.Col(
                            html.H2(
                                "Team-wise Unit-Testing Analytics",
                                className="text-center",
                            ),
                            className="mb-4",
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.H5(
                                "Select a team to see the stats",
                                className="text-center",
                            ),
                            className="mb-4",
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Dropdown(
                                teamList,
                                placeholder="Type Team Name...",
                                clearable=False,
                                id="team-dropdown-exportpage",
                            )
                        ),
                        dbc.Col(
                            dcc.Dropdown(
                                [
                                    "Date-wise Aggregation",
                                    "Week-wise Aggregation",
                                    "Month-wise Aggregation",
                                ],
                                "Date-wise Aggregation",
                                clearable=False,
                                id="timePeriod-dropdown-teamexportpage",
                            )
                        ),
                    ],
                    className="mb-5",
                ),
                dcc.Store(id="team_analytics_df"),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                children=[
                                    html.H4(
                                        children="Team-wise Analytics as per the above filter",
                                        className="text-center",
                                    ),
                                    dbc.Button(
                                        "Download as Excel",
                                        id="team_button_xlsx",
                                        color="primary",
                                        className="mt-3",
                                    ),
                                ],
                                body=True,
                                color="dark",
                                outline=True,
                            ),
                            className="mb-4",
                        ),
                    ]
                ),
                dcc.Download(id="team_analytics_download_xlsx"),
                dbc.Row(
                    [
                        dbc.Col(
                            html.H2(
                                "Select a team to see the stats of its developers",
                                className="text-center",
                            ),
                            className="mb-4",
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.H5(
                                children="DateRange of below Stats, From: "
                                + str(min_date)[0:10]
                                + " To: "
                                + str(max_date)[0:10],
                                className="text-center",
                            ),
                            className="mb-5",
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Dropdown(
                                teamList,
                                placeholder="Type Team Name...",
                                clearable=False,
                                id="teamdev-dropdown-exportpage",
                            )
                        ),
                    ],
                    className="mb-5",
                ),
                dcc.Store(id="teamdev_analytics_df"),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                children=[
                                    html.H4(
                                        children="Team-wise Developer Analytics as per the above filter",
                                        className="text-center",
                                    ),
                                    dbc.Button(
                                        "Download as Excel",
                                        id="teamdev_button_xlsx",
                                        color="primary",
                                        className="mt-3",
                                    ),
                                ],
                                body=True,
                                color="dark",
                                outline=True,
                            ),
                            className="mb-4",
                        ),
                    ]
                ),
                dcc.Download(id="teamdev_analytics_download_xlsx"),
                html.A(
                    "Created by Prabhav Shah",
                    href="https://www.linkedin.com/in/prabhav-shah-7723281a0",
                ),
            ]
        )
    ]
)

# callback to get JSONfied for overall analytics for the given DateRange
@app.callback(
    Output("overall_analytics_df", "data"),
    Input("timePeriod-dropdown-exportpage1", "value"),
    Input("exp-date-picker-range", "start_date"),
    Input("exp-date-picker-range", "end_date"),
)
def dfjson_overall_exportpage(value, startdate, enddate):
    global dfjson_overall
    dfjson_overall = exportpage_row1(value, startdate, enddate)
    return dfjson_overall


# callback to get the above file downloaded as excel on clicking the button
@app.callback(
    Output("overall_analytics_download_xlsx", "data"),
    Input("overall_button_xlsx", "n_clicks"),
    prevent_initial_call=True,
)
def donwload_overall(n_clicks):
    df = pd.read_json(dfjson_overall, orient="split")
    return dcc.send_data_frame(df.to_excel, filename="overall_analytics_download.xlsx")


# callback to get JSONfied for developer-wise analytics for the given DateRange
@app.callback(
    Output("dev_analytics_df", "data"),
    Input("devMail-dropdown-exportpage", "value"),
    Input("timePeriod-dropdown-devexportpage", "value"),
    Input("exp-date-picker-range", "start_date"),
    Input("exp-date-picker-range", "end_date"),
    prevent_initial_call=True,
)
def dfjson_dev_exportpage(email, timeperiod, startdate, enddate):
    global dfjson_dev
    dfjson_dev = exportpage_row2(email, timeperiod, startdate, enddate)
    return dfjson_dev


# callback to get the above file downloaded as excel on clicking the button
@app.callback(
    Output("dev_analytics_download_xlsx", "data"),
    Input("dev_button_xlsx", "n_clicks"),
    prevent_initial_call=True,
)
def donwload_overall(n_clicks):
    df = pd.read_json(dfjson_dev, orient="split")
    return dcc.send_data_frame(df.to_excel, filename="dev_analytics_download.xlsx")


# callback to get JSONfied for team-wise analytics for the given DateRange
@app.callback(
    Output("team_analytics_df", "data"),
    Input("team-dropdown-exportpage", "value"),
    Input("timePeriod-dropdown-teamexportpage", "value"),
    Input("exp-date-picker-range", "start_date"),
    Input("exp-date-picker-range", "end_date"),
    prevent_initial_call=True,
)
def dfjson_dev_exportpage(teamname, timeperiod, startdate, enddate):
    global dfjson_team
    dfjson_team = exportpage_row3(teamname, timeperiod, startdate, enddate)
    return dfjson_team


# callback to get the above file downloaded as excel on clicking the button
@app.callback(
    Output("team_analytics_download_xlsx", "data"),
    Input("team_button_xlsx", "n_clicks"),
    prevent_initial_call=True,
)
def donwload_overall(n_clicks):
    df = pd.read_json(dfjson_team, orient="split")
    return dcc.send_data_frame(df.to_excel, filename="team_analytics_download.xlsx")


# callback to get JSONfied for developer-wise count testcases for the selected team
@app.callback(
    Output("teamdev_analytics_df", "data"),
    Input("teamdev-dropdown-exportpage", "value"),
    prevent_initial_call=True,
)
def dfjson_dev_exportpage(teamname):
    global dfjson_teamdev
    dfjson_teamdev = exportpage_row4(teamname)
    return dfjson_teamdev


# callback to get the above file downloaded as excel on clicking the button
@app.callback(
    Output("teamdev_analytics_download_xlsx", "data"),
    Input("teamdev_button_xlsx", "n_clicks"),
    prevent_initial_call=True,
)
def donwload_overall(n_clicks):
    df = pd.read_json(dfjson_teamdev, orient="split")
    return dcc.send_data_frame(df.to_excel, filename="teamdev_analytics_download.xlsx")
