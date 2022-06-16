# importing libraries
from dash.dependencies import Input, Output
from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import datetime as dt
from datetime import date
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

    # getting total testcases added, deleted, effective, total teams, total devs using homepage function
    totalAdded, totalDeleted, totalEffective = homepage_row1()
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
                                    children="This app marks my very first attempt at using Plotly, Dash and Elasticsearch! "
                                ),
                                className="mb-4",
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H5(
                                    children="It consists of three main pages: Developer-wise, which helps you analyse the unit-testing data for specific developer, also provides the feature to do compariosn between developers; "
                                    "Team-wise, which gives an overview of data team-wise, also display the info for the developers within a team; "
                                    "Export, which helps download dropdown filtered data as Excel."
                                ),
                                className="mb-5",
                            )
                        ]
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
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H1("Overall Analytics", className="text-center"),
                                className="mb-5 mt-5",
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
                                dbc.Card(
                                    children=[
                                        html.H6(
                                            children="Total Unit Test Cases Added",
                                            className="text-center",
                                        ),
                                        html.H1(
                                            children=totalAdded, className="text-center"
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
                                            children=totalDeleted,
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
                                            children=totalEffective,
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
                    # date range picker to filter the data using date-range.
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
                            dbc.Col(dbc.Card(), className="mb-5"),
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
                                className="mb-5",
                            ),
                            dbc.Col(dbc.Card(), className="mb-5"),
                        ],
                        className="mb-5",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H3(
                                    "Plot of Overall Analytics in the selected Date Range",
                                    className="text-center",
                                ),
                                className="mb-5",
                            )
                        ]
                    ),
                    # dropdown for date-wise, week-wise, month-wise aggregation
                    dcc.Dropdown(
                        [
                            "Date-wise Aggregation",
                            "Week-wise Aggregation",
                            "Month-wise Aggregation",
                        ],
                        "Date-wise Aggregation",
                        clearable=False,
                        id="timePeriod-dropdown",
                    ),
                    dcc.Graph(id="overall_analytics"),
                    html.A(
                        "Created by Prabhav Shah",
                        href="https://www.linkedin.com/in/prabhav-shah-7723281a0",
                    ),
                ]
            )
        ]
    )


layout = home_layout()

# callback to plot a graph of overall analytics
@app.callback(
    Output("overall_analytics", "figure"),
    Input("timePeriod-dropdown", "value"),
    Input("home-date-picker-range", "start_date"),
    Input("home-date-picker-range", "end_date"),
)
def get_figure_homepage(value, startdate, enddate):
    fig = homepage_row3(value, startdate, enddate)
    return fig
