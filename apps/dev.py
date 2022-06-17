# importing libraries
from tkinter.tix import DisplayStyle
from dash.dependencies import Input, Output
from numpy import flexible
from devpage import devpage_row1, devpage_row2, devpage_row3, devpage_row4
from dash import html, dcc
import dash_bootstrap_components as dbc
from homepage import homepage_row0
from datetime import datetime as dt
from datetime import date
from app import app

# layout of dev page
def dev_layout():
    # getting minimum and maximum date in provided data using homepage function
    min_date, max_date = homepage_row0()
    min_datem = dt.strptime(str(min_date), "%Y-%m-%d %H:%M:%S")
    max_datem = dt.strptime(str(max_date), "%Y-%m-%d %H:%M:%S")

    # getting list of all developers from the provided data
    devEmailList = devpage_row1()

    # layout of dev-page
    return html.Div(
        [
            dbc.Container(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H1(
                                    "Developer-wise Unit-Testing Analytics",
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
                                            children="Total Developers",
                                            className="text-center",
                                        ),
                                        html.H1(
                                            children=len(devEmailList),
                                            className="text-center",
                                        ),
                                    ],
                                    body=True,
                                    color="primary",
                                    outline=True,
                                ),
                                align="center",
                                className="mb-4",
                            ),
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
                                    "(for individual developer stats and comparison between 2 developers)",
                                    className="text-center",
                                ),
                                className="mb-5",
                            )
                        ]
                    ),
                    # date range picker to filter the data using date-range.
                    dbc.Row(
                        [
                            dbc.Col(dbc.Card(), className="mb-4"),
                            dbc.Col(
                                dbc.Card(
                                    children=[
                                        dcc.DatePickerRange(
                                            id="dev1-date-picker-range",
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
                                html.H3(
                                    "Plot of Developer-wise Analytics in the selected Date Range",
                                    className="text-center",
                                ),
                                className="mb-5",
                            )
                        ]
                    ),
                    # dropdown to select email ID of Sprinklr Employee
                    dcc.Dropdown(
                        devEmailList,
                        placeholder="Type Sprinklr Email ID of Developer...",
                        id="devMail-dropdown",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Card(
                                    children=[
                                        html.H3(
                                            children="Team", className="text-center"
                                        ),
                                        html.H1(
                                            id="teamOfDev", className="text-center"
                                        ),
                                    ],
                                    body=True,
                                    color="dark",
                                    outline=True,
                                ),
                                className="mb-4",
                            ),
                        ],
                        className="mb-5 mt-5",
                    ),
                    # stats of Developer in the selected DateRange
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
                                            id="totalAdded", className="text-center"
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
                                        html.H6(
                                            children="Total Unit Test Cases Deleted",
                                            className="text-center",
                                        ),
                                        html.H1(
                                            id="totalDeleted", className="text-center"
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
                                        html.H6(
                                            children="Total Effective Unit Test Cases",
                                            className="text-center",
                                        ),
                                        html.H1(
                                            id="totalEffective", className="text-center"
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
                    # dropdown for date-wise, week-wise, month-wise aggregation
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
                                    id="timePeriodDev-dropdown",
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
                                    id="testCaseDev-dropdown",
                                )
                            ),
                        ],
                        className="mb-5",
                    ),
                    dcc.Graph(id="dev-analytics"),
                    dbc.Row(),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H3(
                                    "Comparison between 2 Developers in the selected Date Range",
                                    className="text-center",
                                ),
                                className="mb-5",
                            )
                        ]
                    ),
                    # select two maild IDs to create a comparison plot
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Dropdown(
                                    devEmailList,
                                    placeholder="Type Sprinklr Email ID of Developer 1...",
                                    clearable=False,
                                    id="devMail-dropdown-1",
                                )
                            ),
                            dbc.Col(
                                dcc.Dropdown(
                                    devEmailList,
                                    placeholder="Type Sprinklr Email ID of Developer 2...",
                                    clearable=False,
                                    id="devMail-dropdown-2",
                                )
                            ),
                        ],
                        className="mb-5",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Dropdown(
                                    [
                                        "Effective Test Cases",
                                        "Test Cases Added",
                                        "Test Cases Deleted",
                                    ],
                                    "Effective Test Cases",
                                    clearable=False,
                                    id="testCaseDev-dropdown-2",
                                )
                            ),
                        ],
                        className="mb-5",
                    ),
                    dcc.Graph(id="dev-comparison"),
                    html.A(
                        "Created by Prabhav Shah",
                        href="https://www.linkedin.com/in/prabhav-shah-7723281a0",
                    ),
                ]
            )
        ]
    )


layout = dev_layout()

# callback to get the stats of Developer in the given DateRange
@app.callback(
    Output("teamOfDev", "children"),
    Output("totalEffective", "children"),
    Output("totalAdded", "children"),
    Output("totalDeleted", "children"),
    Input("devMail-dropdown", "value"),
    Input("dev1-date-picker-range", "start_date"),
    Input("dev1-date-picker-range", "end_date"),
)
def get_dev_info(devMail, startdate, enddate):
    teamOfDev, effectiveTCbyDev, addedTCbyDev, deletedTCbyDev = devpage_row2(
        devMail, startdate, enddate
    )
    return teamOfDev, effectiveTCbyDev, addedTCbyDev, deletedTCbyDev


# callback to plot a graph of Developer-wise Analytics in the given DateRange
@app.callback(
    Output("dev-analytics", "figure"),
    Input("timePeriodDev-dropdown", "value"),
    Input("testCaseDev-dropdown", "value"),
    Input("devMail-dropdown", "value"),
    Input("dev1-date-picker-range", "start_date"),
    Input("dev1-date-picker-range", "end_date"),
)
def get_Dev_Figure(timePeriod, testCaseType, givenEmailID, startdate, enddate):
    fig = devpage_row3(timePeriod, testCaseType, givenEmailID, startdate, enddate)
    return fig


# callback to plot a graph of comparison between two developers in the given DateRange
@app.callback(
    Output("dev-comparison", "figure"),
    Input("devMail-dropdown-1", "value"),
    Input("devMail-dropdown-2", "value"),
    Input("testCaseDev-dropdown-2", "value"),
    Input("dev1-date-picker-range", "start_date"),
    Input("dev1-date-picker-range", "end_date"),
)
def get_Dev_Comparison(givenEmailID1, givenEmailID2, testCaseType, startdate, enddate):
    fig = devpage_row4(givenEmailID1, givenEmailID2, testCaseType, startdate, enddate)
    return fig
