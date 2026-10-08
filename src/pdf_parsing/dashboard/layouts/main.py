from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback

from pdf_parsing.dashboard.layouts.queue import layout as queue_layout
from pdf_parsing.dashboard.layouts.validation import layout as validation_layout
from pdf_parsing.dashboard.layouts.tuning import layout as tuning_layout
from pdf_parsing.dashboard.layouts.history import layout as history_layout

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

def create_main_layout() -> html.Div:
    sidebar = html.Div(
        [
            html.H2("PDF Parsing", className="display-6"),
            html.Hr(),
            html.P("Human-in-the-loop Pipeline", className="lead"),
            dbc.Nav(
                [
                    dbc.NavLink("Queue", href="/", active="exact"),
                    dbc.NavLink("Validation", href="/validation", active="exact"),
                    dbc.NavLink("Prompt Tuning", href="/tuning", active="exact"),
                    dbc.NavLink("History", href="/history", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        style=SIDEBAR_STYLE,
    )

    content = html.Div(id="page-content", style=CONTENT_STYLE)

    return html.Div([dcc.Location(id="url"), sidebar, content])

@callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return queue_layout()
    elif pathname == "/validation":
        return validation_layout()
    elif pathname == "/tuning":
        return tuning_layout()
    elif pathname == "/history":
        return history_layout()
    return dbc.Container(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )
