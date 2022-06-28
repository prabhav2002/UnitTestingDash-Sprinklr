# importing libraries
from dash.dependencies import Input, Output
from dash import html, dcc
import dash
import pandas as pd
import dash_bootstrap_components as dbc
from dateutil.relativedelta import relativedelta
from datetime import datetime as dt
from datetime import date, timedelta
from homepage import (
    homepage_row0,
    homepage_row1,
    homepage_row2,
    homepage_row3,
)
from app import app

# layout of homepage
def home_layout():
    # getting minimum and maximum date in provided data using homepage function
    min_date, max_date = homepage_row0()
    min_datem = dt.strptime(str(min_date), "%Y-%m-%d %H:%M:%S")
    max_datem = dt.strptime(str(max_date), "%Y-%m-%d %H:%M:%S")

    # getting total teams, total devs using homepage function
    totalDevs, totalTeams = homepage_row2()

    # layout of homepage
    return html.Div(
        [
            dbc.Container(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H1(
                                    "Welcome to Sprinklr Unit-Testing Dashboard",
                                    className="text-center",
                                ),
                                className="mb-5 mt-5",
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H5(
                                    children="The Dashboard is divided into 4 pages. "
                                ),
                                className="text-center mt-5 mb-5",
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Card(
                                    children=[
                                        html.H4(
                                            children="Home",
                                            className="text-center",
                                        ),
                                        html.H6(
                                            children="Total Teams, Total Devs",
                                        ),
                                        html.H6(
                                            children="Overall Unit Testing Analytics",
                                        ),
                                    ],
                                    body=True,
                                    color="primary",
                                    outline=True,
                                ),
                                className="mb-4",
                            ),
                            dbc.Col(
                                dbc.Card(
                                    children=[
                                        html.H4(
                                            children="Developer-wise",
                                            className="text-center",
                                        ),
                                        html.H6(
                                            children="Developer Analytics",
                                        ),
                                        html.H6(
                                            children="Comparison between 2 Developers",
                                        ),
                                    ],
                                    body=True,
                                    color="primary",
                                    outline=True,
                                ),
                                className="mb-4",
                            ),
                            dbc.Col(
                                dbc.Card(
                                    children=[
                                        html.H4(
                                            children="Team-wise",
                                            className="text-center",
                                        ),
                                        html.H6(
                                            children="Team Analytics",
                                        ),
                                        html.H6(
                                            children="Developer Stats for selected Team",
                                        ),
                                    ],
                                    body=True,
                                    color="primary",
                                    outline=True,
                                ),
                                className="mb-4",
                            ),
                            dbc.Col(
                                dbc.Card(
                                    children=[
                                        html.H4(
                                            children="Leaderboard",
                                            className="text-center",
                                        ),
                                        html.H6(
                                            children="Leaderboard Table",
                                        ),
                                        html.H6(
                                            children="with DateRange selection and sorting filters",
                                        ),
                                    ],
                                    body=True,
                                    color="primary",
                                    outline=True,
                                ),
                                className="mb-4",
                            ),
                        ],
                        className="mb-5",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H4(children="General Usage Guidelines:"),
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H6(
                                    children="1. Plots can be saved as PNG from the options given in the right corner of the plot."
                                ),
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H6(
                                    children="2. Data of the plot can be downloaded as Excel from the button given below the plot."
                                ),
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H6(
                                    children="3. Date Range selected will be applicable to the content of the of that page given below the Date Range Picker. "
                                ),
                            )
                        ],
                        className="mb-5",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Card(
                                    children=[
                                        html.H4(
                                            children="Access the code used to build this dashboard",
                                            className="text-center",
                                        ),
                                        dbc.Button(
                                            "GitHub",
                                            href="https://github.com/prabhav2002/UnitTestingDash-Sprinklr",
                                            color="primary",
                                            className="mt-3",
                                        ),
                                    ],
                                    body=True,
                                    color="dark",
                                    outline=True,
                                ),
                                width=6,
                                className="mb-4",
                            ),
                            dbc.Col(
                                dbc.Card(
                                    children=[
                                        html.H4(
                                            children="Read the Medium article detailing the process",
                                            className="text-center",
                                        ),
                                        dbc.Button(
                                            "Medium",
                                            href="https://medium.com/@201901216/unit-testing-analytics-dashboard-using-elasticsearch-and-python-7c0db08da895",
                                            color="primary",
                                            className="mt-3",
                                        ),
                                    ],
                                    body=True,
                                    color="dark",
                                    outline=True,
                                ),
                                width=6,
                                className="mb-4",
                            ),
                        ],
                        className="mb-5",
                    ),
                    # title of the page
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H1(
                                    "Overall Unit Testing Analytics",
                                    className="text-center",
                                ),
                                className="mb-5 mt-5",
                            )
                        ]
                    ),
                    # total teams and total devs stats
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
                                width=6,
                                className="mb-4",
                            ),
                            dbc.Col(
                                dbc.Card(
                                    children=[
                                        html.H2(
                                            children="Total Developers",
                                            className="text-center",
                                        ),
                                        html.H1(
                                            children=totalDevs, className="text-center"
                                        ),
                                    ],
                                    body=True,
                                    color="primary",
                                    outline=True,
                                ),
                                width=6,
                                className="mb-4",
                            ),
                        ],
                        className="mb-5",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H4(
                                    "Select a date range to get the stats of that specific time-period",
                                    className="text-center",
                                ),
                                className="mb-5 mt-5",
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
                                            id="home-date-picker-range",
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
                                        ),
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
                                            id="homedate-btn1",
                                        ),
                                        dbc.Button(
                                            "Last Month",
                                            outline=True,
                                            color="primary",
                                            id="homedate-btn2",
                                        ),
                                    ]
                                ),
                                className="text-center",
                            ),
                            dbc.Col(dbc.Card()),
                        ],
                        className="mb-4 flex center",
                    ),
                    # test cases stats in the given date range
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Card(
                                    children=[
                                        html.H6(
                                            children="Total Unit Test Cases Added",
                                            className="text-center",
                                        ),
                                        html.H1(
                                            id="totalAddedHome", className="text-center"
                                        ),
                                    ],
                                    body=True,
                                    color="dark",
                                    outline=True,
                                ),
                                width=4,
                                className="mb-4",
                            ),
                            dbc.Col(
                                dbc.Card(
                                    children=[
                                        html.H6(
                                            children="Total Unit Test Cases Deleted",
                                            className="text-center",
                                        ),
                                        html.H1(
                                            id="totalDeletedHome",
                                            className="text-center",
                                        ),
                                    ],
                                    body=True,
                                    color="dark",
                                    outline=True,
                                ),
                                width=4,
                                className="mb-4",
                            ),
                            dbc.Col(
                                dbc.Card(
                                    children=[
                                        html.H6(
                                            children="Total Effective Unit Test Cases",
                                            className="text-center",
                                        ),
                                        html.H1(
                                            id="totalEffectiveHome",
                                            className="text-center",
                                        ),
                                    ],
                                    body=True,
                                    color="dark",
                                    outline=True,
                                ),
                                width=4,
                                className="mb-4",
                            ),
                        ],
                        className="mb-5",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H3(
                                    "Plot of Overall Unit Testing Analytics in the selected Date Range",
                                    className="text-center",
                                ),
                                className="mb-5",
                            )
                        ]
                    ),
                    # dropdown for daily, weekly, monthly
                    dcc.Dropdown(
                        [
                            "Daily",
                            "Weekly",
                            "Monthly",
                        ],
                        "Daily",
                        clearable=False,
                        id="timePeriod-dropdown",
                    ),
                    dcc.Graph(id="overall_analytics"),
                    dcc.Store(id="overall_analytics_df"),
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Card(
                                    children=[
                                        html.H4(
                                            children="Overall Unit Testing Analytics as per the above filter",
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
                    html.A(
                        "Created by Prabhav Shah",
                        href="https://www.linkedin.com/in/prabhav-shah-7723281a0",
                    ),
                ]
            )
        ]
    )


layout = home_layout()
# callback to get the test cases stats in the given date range
@app.callback(
    Output("totalAddedHome", "children"),
    Output("totalDeletedHome", "children"),
    Output("totalEffectiveHome", "children"),
    Input("home-date-picker-range", "start_date"),
    Input("home-date-picker-range", "end_date"),
)
def get_testcase_stats(startdate, enddate):
    totalAdded, totalDeleted, totalEffective = homepage_row1(startdate, enddate)
    return str(int(totalAdded)), str(int(totalDeleted)), str(int(totalEffective))


# callback to plot a graph of overall analytics
@app.callback(
    Output("overall_analytics", "figure"),
    Output("overall_analytics_df", "data"),
    Input("timePeriod-dropdown", "value"),
    Input("home-date-picker-range", "start_date"),
    Input("home-date-picker-range", "end_date"),
)
def get_figure_homepage(value, startdate, enddate):
    global dfjson_overall
    fig, dfjson_overall = homepage_row3(value, startdate, enddate)
    return fig, dfjson_overall


# callback to get the above file downloaded as excel on clicking the button
@app.callback(
    Output("overall_analytics_download_xlsx", "data"),
    Input("overall_button_xlsx", "n_clicks"),
    prevent_initial_call=True,
)
def donwload_overall(n_clicks):
    dfOverAll = pd.read_json(dfjson_overall, orient="split")
    return dcc.send_data_frame(
        dfOverAll.to_excel, filename="overall_analytics_download.xlsx"
    )


# callback to get date range
@app.callback(
    Output("home-date-picker-range", "start_date"),
    Output("home-date-picker-range", "end_date"),
    Input("homedate-btn1", "n_clicks"),
    Input("homedate-btn2", "n_clicks"),
    prevent_initial_call=True,
)
def set_date_range_buttons(n_clicks_1, n_clicks_2):
    # getting minimum and maximum date in provided data using homepage function
    min_date_i, max_date_i = homepage_row0()
    ctx = dash.callback_context
    clicked_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if clicked_id == "homedate-btn1":
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
    elif clicked_id == "homedate-btn2":
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
