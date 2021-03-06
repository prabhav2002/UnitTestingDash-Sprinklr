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
    Input("index-date-picker-range", "start_date"),
    Input("index-date-picker-range", "end_date"),
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
