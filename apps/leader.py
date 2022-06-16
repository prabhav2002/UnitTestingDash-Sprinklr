# importing libraries
from dash.dependencies import Input, Output
from dash import dash_table
from app import app
import dash_bootstrap_components as dbc
from datetime import date, timedelta
from datetime import datetime as dt
from dash import dcc, html
from homepage import homepage_row0
from teampage import teampage_row1
from leaderboard import leaderboard_row1

# layout of leaderboard
def leader_layout():
    # getting minimum and maximum date in provided data using homepage function
    min_date, max_date = homepage_row0()
    max_date_minus_week = max_date - timedelta(days=6)
    min_datem = dt.strptime(str(min_date), "%Y-%m-%d %H:%M:%S")
    max_datem = dt.strptime(str(max_date), "%Y-%m-%d %H:%M:%S")
    max_datem_minus_week = dt.strptime(str(max_date_minus_week), "%Y-%m-%d %H:%M:%S")

    # getting total number of teams, name of all the teams, and team-wise developer count
    totalTeams, teamList = teampage_row1()

    # layout of leaderboard
    return html.Div(
        [
            dbc.Container(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H1(
                                    "Leaderboard",
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
                                    "Select a date range to get the leaderboard of that specific time-period",
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
                                            id="leader-date-picker-range",
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
                                                max_datem_minus_week.year,
                                                max_datem_minus_week.month,
                                                max_datem_minus_week.day,
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
                                    teamList,
                                    clearable=False,
                                    id="leader-team-multi-dropdown",
                                    multi=True,
                                )
                            ),
                        ],
                        className="mb-5",
                    ),
                    # data table
                    dbc.Table(
                        id="leaderboard-table",
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


layout = leader_layout()

# callback to get data table of dev-wise analytics for selected teams for the given DateRange
@app.callback(
    Output("leaderboard-table", "children"),
    Input("leader-team-multi-dropdown", "value"),
    Input("leader-date-picker-range", "start_date"),
    Input("leader-date-picker-range", "end_date"),
    prevent_intial_call=True,
)
def df_leaderboard(teamNamesMultiDropdown, startdate, enddate):
    global df
    df = leaderboard_row1(teamNamesMultiDropdown, startdate, enddate)
    return dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        editable=True,
        sort_action="native",
        sort_mode="single",
        sort_by=[{"column_id": "Effective Test Cases", "direction": "desc"}],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=20,
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
