# importing libraries
from dash.dependencies import Input, Output
from functions.teampage import (
    teampage_row1,
    teampage_row2,
    teampage_row3,
    teampage_row4,
)
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from functions.homepage import homepage_row0
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
                                    teamList,
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
                    # data table
                    dbc.Table(
                        id="team_analytics_table", bordered=True, className="mb-5"
                    ),
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
                    # data table
                    dbc.Table(
                        id="teamdev_analytics_table",
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


layout = team_layout()

# callback to get the plot of analytics and JSONfied data for the selected teams in the given DateRange
@app.callback(
    Output("team_analytics", "figure"),
    Output("team_analytics_table", "children"),
    Input("timePeriodteam-dropdown", "value"),
    Input("team-multi-dropdown", "value"),
    Input("testCaseteam-dropdown", "value"),
    Input("index-date-picker-range", "start_date"),
    Input("index-date-picker-range", "end_date"),
)
def get_figure_datatable_teampage(
    timePeriod, teamNamesMultiDropdown, testCaseType, startdate, enddate
):
    fig, df_team = teampage_row3(
        timePeriod, teamNamesMultiDropdown, testCaseType, startdate, enddate
    )
    return fig, dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df_team.columns],
        data=df_team.to_dict("records"),
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


# callback to get the plot of developer-wise count of testcases and JSONfied data for selected team in the selected date range
@app.callback(
    Output("teamWiseDev_analytics", "figure"),
    Output("teamdev_analytics_table", "children"),
    Input("team-dropdown", "value"),
    Input("testCaseteam2-dropdown", "value"),
    Input("index-date-picker-range", "start_date"),
    Input("index-date-picker-range", "end_date"),
)
def get_figure_teamWiseDev(team, testCaseType, startdate, enddate):
    fig, df_teamdev = teampage_row4(team, testCaseType, startdate, enddate)
    return fig, dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df_teamdev.columns],
        data=df_teamdev.to_dict("records"),
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
