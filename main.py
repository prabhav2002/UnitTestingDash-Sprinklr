# importing libraries
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import app
from apps import team, dev, home, export, leader


def main_layout():
    # the style arguments for the sidebar
    SIDEBAR_STYLE = {
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "20rem",
        "padding": "2rem 1rem",
        "background-color": "#f8f9fa",
    }

    # the styles for the main content position it to the right of the sidebar and
    # add some padding.
    CONTENT_STYLE = {
        "margin-left": "18rem",
        "margin-right": "2rem",
        "padding": "2rem 1rem",
    }

    # contents of sidebar
    sidebar = html.Div(
        [
            html.Img(src="/assets/Sprinklr.png", height="50px"),
            html.H2("Dashboard", className="display-4"),
            html.Hr(),
            html.P(
                "A simple dashboard to analyze unit testing of Sprinklr",
                className="lead",
            ),
            html.P("Timezone: Asia/Kolkata", className="lead"),
            # redirection links to other pages of site
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/", active="exact"),
                    dbc.NavLink("Developer-wise", href="/dev", active="exact"),
                    dbc.NavLink("Team-wise", href="/team", active="exact"),
                    dbc.NavLink("Leaderboard", href="/leader", active="exact"),
                    dbc.NavLink("Exports", href="/export", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
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
    elif pathname == "/export":
        return export.export_layout()
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
    app.run_server(debug=True)
