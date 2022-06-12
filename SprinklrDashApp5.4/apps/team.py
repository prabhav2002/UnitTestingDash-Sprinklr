# importing libraries
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from datetime import date
from datetime import datetime as dt
from teampage import teampage_row1, teampage_row2, teampage_row3, teampage_row4
from homepage import homepage_row0
from app import app

# getting minimum and maximum date in provided data using homepage function
min_date, max_date = homepage_row0()
min_datem = dt.strptime(str(min_date), "%Y-%m-%d %H:%M:%S")
max_datem = dt.strptime(str(max_date), "%Y-%m-%d %H:%M:%S")

# getting total number of teams, name of all the teams, and team-wse developer count
totalTeams, teamList = teampage_row1()
teamWiseDevCount = teampage_row2()

# layout of teampage
layout = html.Div(
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
                                        children="Total Teams", className="text-center"
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
                            html.H4(
                                "Let's take a glance on plot to get a idea about number of test cases added/deleted/effective in different time range. Click on labels to activate/deactivate specific team's plot.",
                                className="text-center",
                            ),
                            className="mb-5 mt-5",
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.H6(
                                "Select a date range to get the stats of that specific time-period",
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
                # multi team select dropdown
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Dropdown(
                                teamList,
                                teamList[0],
                                clearable=False,
                                id="team-multi-dropdown",
                                multi=True,
                            )
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
                                    "Date-wise Aggregation",
                                    "Week-wise Aggregation",
                                    "Month-wise Aggregation",
                                ],
                                "Date-wise Aggregation",
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
                dbc.Row(
                    [
                        dbc.Col(
                            html.H4(
                                "Test Cases Stats of Developers group by Teams",
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
                html.A(
                    "Created by Prabhav Shah",
                    href="https://www.linkedin.com/in/prabhav-shah-7723281a0",
                ),
            ]
        )
    ]
)

# callback to get the plot of analytics for the selected teams in the given DateRange
@app.callback(
    Output("team_analytics", "figure"),
    [
        Input("timePeriodteam-dropdown", "value"),
        Input("team-multi-dropdown", "value"),
        Input("testCaseteam-dropdown", "value"),
        Input("team-date-picker-range", "start_date"),
        Input("team-date-picker-range", "end_date"),
    ],
)
def get_figure_teampage(
    timePeriod, teamNamesMultiDropdown, testCaseType, startdate, enddate
):
    fig = teampage_row3(
        timePeriod, teamNamesMultiDropdown, testCaseType, startdate, enddate
    )
    return fig


# callback to get the plot of developer-wise count of testcases in selected team from overall provided data
@app.callback(
    Output("teamWiseDev_analytics", "figure"),
    [
        Input("team-dropdown", "value"),
        Input("testCaseteam2-dropdown", "value"),
    ],
)
def get_figure_teamWiseDev(team, testCaseType):
    fig = teampage_row4(team, testCaseType)
    return fig
