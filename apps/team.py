# importing libraries
from dash.dependencies import Input, Output
from teampage import teampage_row1, teampage_row2, teampage_row3, teampage_row4
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from homepage import homepage_row0
import dash
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta
from app import app

# layout of team page
def team_layout():
    # getting minimum and maximum date in provided data using homepage function
    min_date, max_date = homepage_row0()
    min_datem = dt.strptime(str(min_date), "%Y-%m-%d %H:%M:%S")
    max_datem = dt.strptime(str(max_date), "%Y-%m-%d %H:%M:%S")

    # getting total number of teams, name of all the teams, and team-wse developer count
    totalTeams, teamList = teampage_row1()
    teamWiseDevCount = teampage_row2()

    # layout of teampage
    return html.Div(
        [
            dbc.Container(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H1(
                                    "Team-wise Unit-Testing Analytics",
                                    className="text-center",
                                ),
                                className="mb-5 mt-5",
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Card(
                                    children=[
                                        html.H2(
                                            children="Total Teams",
                                            className="text-center",
                                        ),
                                        html.H1(
                                            children=totalTeams, className="text-center"
                                        ),
                                    ],
                                    body=True,
                                    color="primary",
                                    outline=True,
                                ),
                                width=4,
                                align="center",
                                className="mb-4",
                            ),
                            dbc.Col(dcc.Graph(figure=teamWiseDevCount)),
                        ],
                        className="mb-5",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H3(
                                    "Select a date range to get the stats of that specific time-period",
                                    className="text-center",
                                ),
                                className="mb-5",
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H6(
                                    "(for Team-wise stats as well as stats of developers of selected team)",
                                    className="text-center",
                                ),
                                className="mb-5",
                            )
                        ]
                    ),
                    # date range picker to filter the data using date-range.
                    dbc.Row(
                        [
                            dbc.Col(dbc.Card()),
                            dbc.Col(
                                dbc.Card(
                                    children=[
                                        dcc.DatePickerRange(
                                            id="team-date-picker-range",
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
                                                max_datem.year,
                                                max_datem.month,
                                                max_datem.day,
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
                                className="text-center",
                            ),
                            dbc.Col(dbc.Card()),
                        ],
                        className="mb-2",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(dbc.Card()),
                            dbc.Col(
                                dbc.ButtonGroup(
                                    [
                                        dbc.Button(
                                            "Last 7 Days",
                                            outline=True,
                                            color="primary",
                                            id="teamdate-btn1",
                                        ),
                                        dbc.Button(
                                            "Last Month",
                                            outline=True,
                                            color="primary",
                                            id="teamdate-btn2",
                                        ),
                                    ]
                                ),
                                className="text-center",
                            ),
                            dbc.Col(dbc.Card()),
                        ],
                        className="mb-4 flex center",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H3(
                                    "Plot of Team-wise Analytics in the selected Date Range",
                                    className="text-center",
                                ),
                                className="mb-5",
                            )
                        ]
                    ),
                    # multi team select dropdown
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Dropdown(
                                    teamList,
                                    teamList[0],
                                    clearable=False,
                                    placeholder="Select Team(s) to get the stats...",
                                    id="team-multi-dropdown",
                                    multi=True,
                                )
                            ),
                        ],
                        className="mb-5",
                    ),
                    # dropdown for daily, weekly, monthly, and dropdown for test cases types
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Dropdown(
                                    [
                                        "Daily",
                                        "Weekly",
                                        "Monthly",
                                    ],
                                    "Daily",
                                    clearable=False,
                                    id="timePeriodteam-dropdown",
                                )
                            ),
                            dbc.Col(
                                dcc.Dropdown(
                                    [
                                        "Effective Test Cases",
                                        "Test Cases Added",
                                        "Test Cases Deleted",
                                    ],
                                    "Effective Test Cases",
                                    clearable=False,
                                    id="testCaseteam-dropdown",
                                )
                            ),
                        ],
                        className="mb-5",
                    ),
                    dcc.Graph(id="team_analytics"),
                    # downloading team-wise data as excel
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
                                html.H3(
                                    "Plot of Developer-wise Analytics for the selected team in the selected Date Range",
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
                                    teamList[0],
                                    clearable=False,
                                    id="team-dropdown",
                                )
                            ),
                            dbc.Col(
                                dcc.Dropdown(
                                    [
                                        "Effective Test Cases",
                                        "Test Cases Added",
                                        "Test Cases Deleted",
                                    ],
                                    "Effective Test Cases",
                                    clearable=False,
                                    id="testCaseteam2-dropdown",
                                )
                            ),
                        ],
                        className="mb-5",
                    ),
                    dcc.Graph(id="teamWiseDev_analytics"),
                    # downlaoding dev-wise analytics for selected team as excel
                    dcc.Store(id="teamdev_analytics_df"),
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Card(
                                    children=[
                                        html.H4(
                                            children="Developer-wise Analytics of the selected Team as per the above filter",
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


layout = team_layout()

# callback to get the plot of analytics and JSONfied data for the selected teams in the given DateRange
@app.callback(
    Output("team_analytics", "figure"),
    Output("team_analytics_df", "data"),
    Input("timePeriodteam-dropdown", "value"),
    Input("team-multi-dropdown", "value"),
    Input("testCaseteam-dropdown", "value"),
    Input("team-date-picker-range", "start_date"),
    Input("team-date-picker-range", "end_date"),
)
def get_figure_teampage(
    timePeriod, teamNamesMultiDropdown, testCaseType, startdate, enddate
):
    global dfjson_team
    fig, dfjson_team = teampage_row3(
        timePeriod, teamNamesMultiDropdown, testCaseType, startdate, enddate
    )
    return fig, dfjson_team


# callback to get the above file downloaded as excel on clicking the button
@app.callback(
    Output("team_analytics_download_xlsx", "data"),
    Input("team_button_xlsx", "n_clicks"),
    prevent_initial_call=True,
)
def donwload_overall(n_clicks):
    dfTeam = pd.read_json(dfjson_team, orient="split")
    return dcc.send_data_frame(dfTeam.to_excel, filename="team_analytics_download.xlsx")


# callback to get the plot of developer-wise count of testcases and JSONfied data for selected team in the selected date range
@app.callback(
    Output("teamWiseDev_analytics", "figure"),
    Output("teamdev_analytics_df", "data"),
    Input("team-dropdown", "value"),
    Input("testCaseteam2-dropdown", "value"),
    Input("team-date-picker-range", "start_date"),
    Input("team-date-picker-range", "end_date"),
)
def get_figure_teamWiseDev(team, testCaseType, startdate, enddate):
    global dfjson_teamdev
    fig, dfjson_teamdev = teampage_row4(team, testCaseType, startdate, enddate)
    return fig, dfjson_teamdev


# callback to get the above file downloaded as excel on clicking the button
@app.callback(
    Output("teamdev_analytics_download_xlsx", "data"),
    Input("teamdev_button_xlsx", "n_clicks"),
    prevent_initial_call=True,
)
def donwload_overall(n_clicks):
    dfTeamDev = pd.read_json(dfjson_teamdev, orient="split")
    return dcc.send_data_frame(
        dfTeamDev.to_excel, filename="teamdev_analytics_download.xlsx"
    )


# callback to get date range
@app.callback(
    Output("team-date-picker-range", "start_date"),
    Output("team-date-picker-range", "end_date"),
    Input("teamdate-btn1", "n_clicks"),
    Input("teamdate-btn2", "n_clicks"),
    prevent_initial_call=True,
)
def set_date_range_buttons(n_clicks_1, n_clicks_2):
    # getting minimum and maximum date in provided data using homepage function
    min_date_i, max_date_i = homepage_row0()
    ctx = dash.callback_context
    clicked_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if clicked_id == "teamdate-btn1":
        min_date = min_date_i
        max_date = max_date_i
        max_date_minus = max_date - relativedelta(days=6)
        min_date = max(min_date, max_date_minus)
        min_datem = dt.strptime(str(min_date), "%Y-%m-%d %H:%M:%S")
        max_datem = dt.strptime(str(max_date), "%Y-%m-%d %H:%M:%S")
        return (
            date(
                min_datem.year,
                min_datem.month,
                min_datem.day,
            ),
            date(
                max_datem.year,
                max_datem.month,
                max_datem.day,
            ),
        )
    elif clicked_id == "teamdate-btn2":
        min_date = min_date_i
        max_date = max_date_i
        last_day_of_prev_month = max_date.replace(day=1) - timedelta(days=1)
        start_day_of_prev_month = max_date.replace(day=1) - timedelta(
            days=last_day_of_prev_month.day
        )
        min_date = max(min_date, start_day_of_prev_month)
        max_date = min(max_date, last_day_of_prev_month)
        min_datem = dt.strptime(str(min_date), "%Y-%m-%d %H:%M:%S")
        max_datem = dt.strptime(str(max_date), "%Y-%m-%d %H:%M:%S")
        return (
            date(
                min_datem.year,
                min_datem.month,
                min_datem.day,
            ),
            date(
                max_datem.year,
                max_datem.month,
                max_datem.day,
            ),
        )
    else:
        min_date = min_date_i
        max_date = max_date_i
        min_datem = dt.strptime(str(min_date), "%Y-%m-%d %H:%M:%S")
        max_datem = dt.strptime(str(max_date), "%Y-%m-%d %H:%M:%S")
        return (
            date(
                min_datem.year,
                min_datem.month,
                min_datem.day,
            ),
            date(
                max_datem.year,
                max_datem.month,
                max_datem.day,
            ),
        )
