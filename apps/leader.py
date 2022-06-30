# importing libraries
from dash.dependencies import Input, Output
from dash import dash_table
from app import app
import dash_bootstrap_components as dbc
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from datetime import datetime as dt
from dash import dcc, html
import dash
from functions.homepage import homepage_row0
from functions.teampage import teampage_row1
from functions.leaderboard import leaderboard_row1

# layout of leaderboard
def leader_layout():
    # getting minimum and maximum date in provided data using homepage function
    min_date, max_date = homepage_row0()
    max_date_minus_week = max_date - timedelta(days=6)
    min_datem = dt.strptime(str(min_date), "%Y-%m-%d %H:%M:%S")
    max_datem = dt.strptime(str(max_date), "%Y-%m-%d %H:%M:%S")
    max_datem_minus_week = dt.strptime(str(max_date_minus_week), "%Y-%m-%d %H:%M:%S")

    # getting total number of teams, name of all the teams, and team-wise developer count
    global teamList
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
                            dbc.Col(dbc.Card()),
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
                                                max_datem.year,
                                                max_datem.month,
                                                max_datem.day,
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
                                            id="leaderdate-btn1",
                                        ),
                                        dbc.Button(
                                            "Last Month",
                                            outline=True,
                                            color="primary",
                                            id="leaderdate-btn2",
                                        ),
                                    ]
                                ),
                                className="text-center",
                            ),
                            dbc.Col(dbc.Card()),
                        ],
                        className="mb-4 flex center",
                    ),
                    # multi team select dropdown
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Dropdown(
                                    teamList,
                                    teamList,
                                    clearable=False,
                                    placeholder="Select Team(s) to get the leaderboard table...",
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
)
def df_leaderboard(teamNamesMultiDropdown, startdate, enddate):
    df_leader = leaderboard_row1(teamNamesMultiDropdown, startdate, enddate)
    return dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df_leader.columns],
        data=df_leader.to_dict("records"),
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


# callback to get date range
@app.callback(
    Output("leader-date-picker-range", "start_date"),
    Output("leader-date-picker-range", "end_date"),
    Input("leaderdate-btn1", "n_clicks"),
    Input("leaderdate-btn2", "n_clicks"),
    prevent_initial_call=True,
)
def set_date_range_buttons(n_clicks_1, n_clicks_2):
    # getting minimum and maximum date in provided data using homepage function
    min_date_i, max_date_i = homepage_row0()
    ctx = dash.callback_context
    clicked_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if clicked_id == "leaderdate-btn1":
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
    elif clicked_id == "leaderdate-btn2":
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
