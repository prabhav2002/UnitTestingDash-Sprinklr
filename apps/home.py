# importing libraries
from dash.dependencies import Input, Output
from dash import html, dcc, dash_table
import dash
import dash_bootstrap_components as dbc
from dateutil.relativedelta import relativedelta
from datetime import datetime as dt
from datetime import date, timedelta
from functions.homepage import (
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
                                className="mt-5",
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H5(
                                    children="The Dashboard is divided into 4 pages. "
                                ),
                                className="text-center mt-4 mb-4",
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
                        className="mb-4",
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
                                    children="2. Data of the plot can be downloaded as Excel from the button given above the data table."
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
                        className="mb-3",
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
                        className="mb-4",
                    ),
                    # title of the page
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H1(
                                    "Overall Unit Testing Analytics",
                                    className="text-center",
                                ),
                                className="mb-5",
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
                        className="mb-4",
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
                    # data table
                    dbc.Table(
                        id="homepage-table",
                        bordered=True,
                    ),
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
    Input("index-date-picker-range", "start_date"),
    Input("index-date-picker-range", "end_date"),
)
def get_testcase_stats(startdate, enddate):
    totalAdded, totalDeleted, totalEffective = homepage_row1(startdate, enddate)
    return str(int(totalAdded)), str(int(totalDeleted)), str(int(totalEffective))


# callback to get the plot and the data table of overall unit testing analytics for the given DateRange
@app.callback(
    Output("overall_analytics", "figure"),
    Output("homepage-table", "children"),
    Input("timePeriod-dropdown", "value"),
    Input("index-date-picker-range", "start_date"),
    Input("index-date-picker-range", "end_date"),
)
def get_fig_table_homepage(value, startdate, enddate):
    fig, df_home = homepage_row3(value, startdate, enddate)
    return fig, dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df_home.columns],
        data=df_home.to_dict("records"),
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
