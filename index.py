# importing libraries
from dash import html, dcc
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import app, server
from apps import team, dev, home, leader
from environment.settings import APP_HOST, APP_PORT, APP_DEBUG, DEV_TOOLS_PROPS_CHECK
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta
from functions.homepage import homepage_row0


def main_layout():

    # getting minimum and maximum date in provided data using homepage function
    min_date, max_date = homepage_row0()
    min_datem = dt.strptime(str(min_date), "%Y-%m-%d %H:%M:%S")
    max_datem = dt.strptime(str(max_date), "%Y-%m-%d %H:%M:%S")

    # the style arguments for the sidebar
    SIDEBAR_STYLE = {
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "23rem",
        "padding": "2rem 1rem",
        "background-color": "#f8f9fa",
    }

    # the styles for the main content position it to the right of the sidebar and
    # add some padding.
    CONTENT_STYLE = {
        "margin-left": "25rem",
        "margin-right": "2rem",
        "padding": "2rem 1rem",
    }

    # contents of sidebar
    sidebar = html.Div(
        [
            html.Img(src="/assets/Sprinklr.png", alt="Sprinklr", height="50px"),
            html.H2("Dashboard", className="display-4"),
            html.Hr(),
            html.P(
                "A simple dashboard to analyze unit testing of Sprinklr",
                className="lead",
            ),
            # redirection links to other pages of site
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/", active="exact"),
                    dbc.NavLink("Developer-wise", href="/dev", active="exact"),
                    dbc.NavLink("Team-wise", href="/team", active="exact"),
                    dbc.NavLink("Leaderboard", href="/leader", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
            html.Hr(),
            # date range picker to filter the data using date-range.
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            children=[
                                dcc.DatePickerRange(
                                    id="index-date-picker-range",
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
                                )
                            ],
                            body=True,
                            color="primary",
                            outline=True,
                        ),
                        className="text-center",
                    ),
                ],
                className="mb-2",
            ),
            # options for date range
            dbc.Row(
                [
                    dbc.Col(
                        dbc.ButtonGroup(
                            [
                                dbc.Button(
                                    "Last 7 Days",
                                    outline=True,
                                    color="primary",
                                    id="indexdate-btn1",
                                ),
                                dbc.Button(
                                    "Last Month",
                                    outline=True,
                                    color="primary",
                                    id="indexdate-btn2",
                                ),
                                dbc.Button(
                                    "Overall",
                                    outline=True,
                                    color="primary",
                                    id="indexdate-btn3",
                                ),
                            ]
                        ),
                        className="text-center",
                    ),
                ],
                className="mb-4 flex center",
            ),
            html.P("Timezone: Asia/Kolkata", className="lead"),
            html.Hr(),
            html.A(
                "Github", href="https://github.com/prabhav2002/UnitTestingDash-Sprinklr"
            ),
            html.Hr(),
            html.A(
                "Medium",
                href="https://medium.com/@201901216/unit-testing-analytics-dashboard-using-elasticsearch-and-python-7c0db08da895",
            ),
            html.Hr(),
            html.A(
                "Created by Prabhav Shah",
                href="https://www.linkedin.com/in/prabhav-shah-7723281a0",
            ),
        ],
        style=SIDEBAR_STYLE,
    )

    content = html.Div(id="page-content", style=CONTENT_STYLE)

    return html.Div([dcc.Location(id="url"), sidebar, content])


app.layout = main_layout

# callback for redirection
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return home.home_layout()
    elif pathname == "/dev":
        return dev.dev_layout()
    elif pathname == "/team":
        return team.team_layout()
    elif pathname == "/leader":
        return leader.leader_layout()
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


# callback to get date range
@app.callback(
    Output("index-date-picker-range", "start_date"),
    Output("index-date-picker-range", "end_date"),
    Input("indexdate-btn1", "n_clicks"),
    Input("indexdate-btn2", "n_clicks"),
    Input("indexdate-btn3", "n_clicks"),
    prevent_initial_call=True,
)
def set_date_range_buttons(n_clicks_1, n_clicks_2, n_clicks_3):
    # getting minimum and maximum date in provided data using homepage function
    min_date_i, max_date_i = homepage_row0()
    ctx = dash.callback_context
    clicked_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if clicked_id == "indexdate-btn1":
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
    elif clicked_id == "indexdate-btn2":
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


if __name__ == "__main__":
    app.run_server(
        host=APP_HOST,
        port=APP_PORT,
        debug=APP_DEBUG,
        dev_tools_props_check=DEV_TOOLS_PROPS_CHECK,
    )
