# importing libraries
from dash.dependencies import Input, Output
from functions.devpage import (
    devpage_row1,
    devpage_row2,
    devpage_row3,
    devpage_row4,
)
from dash import html, dcc, dash_table
import dash
import dash_bootstrap_components as dbc
from functions.homepage import homepage_row0
from datetime import datetime as dt
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
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
                    # title
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
                    # total devs
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
                    # dropdown for daily, weekly, monthly and dropdown for test-cases type
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
                    # data table
                    dbc.Table(
                        id="dev_analytics_table",
                        bordered=True,
                        className="mb-5",
                    ),
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
                    # select two mail IDs to create a comparison plot
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
    Input("index-date-picker-range", "start_date"),
    Input("index-date-picker-range", "end_date"),
)
def get_dev_info(devMail, startdate, enddate):
    teamOfDev, effectiveTCbyDev, addedTCbyDev, deletedTCbyDev = devpage_row2(
        devMail, startdate, enddate
    )
    return teamOfDev, effectiveTCbyDev, addedTCbyDev, deletedTCbyDev


# callback to plot a graph and get datatable of Developer-wise Analytics in the given DateRange
@app.callback(
    Output("dev-analytics", "figure"),
    Output("dev_analytics_table", "children"),
    Input("timePeriodDev-dropdown", "value"),
    Input("testCaseDev-dropdown", "value"),
    Input("devMail-dropdown", "value"),
    Input("index-date-picker-range", "start_date"),
    Input("index-date-picker-range", "end_date"),
)
def get_Dev_Figure(timePeriod, testCaseType, givenEmailID, startdate, enddate):
    fig, df_dev = devpage_row3(
        timePeriod, testCaseType, givenEmailID, startdate, enddate
    )
    return fig, dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df_dev.columns],
        data=df_dev.to_dict("records"),
        editable=True,
        sort_action="native",
        sort_mode="single",
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
        export_format="xlsx",
        style_cell={"padding": "5px", "textAlign": "left"},
        style_header={
            "backgroundColor": "#037bff",
            "fontWeight": "bold",
            "color": "#eef5ff",
        },
        style_data_conditional=[
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "#eef5ff",
            },
        ],
    )


# callback to plot a graph of comparison between two developers in the given DateRange
@app.callback(
    Output("dev-comparison", "figure"),
    Input("devMail-dropdown-1", "value"),
    Input("devMail-dropdown-2", "value"),
    Input("testCaseDev-dropdown-2", "value"),
    Input("index-date-picker-range", "start_date"),
    Input("index-date-picker-range", "end_date"),
)
def get_Dev_Comparison(givenEmailID1, givenEmailID2, testCaseType, startdate, enddate):
    fig = devpage_row4(givenEmailID1, givenEmailID2, testCaseType, startdate, enddate)
    return fig
