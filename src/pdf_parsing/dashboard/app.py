from __future__ import annotations

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc

from pdf_parsing.dashboard.layouts.main import create_main_layout
from pdf_parsing.dashboard.callbacks.queue_cb import register_queue_callbacks
# TODO: Import other callbacks here

def create_app() -> dash.Dash:
    app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.FLATLY],
        suppress_callback_exceptions=True,
        use_pages=False,
    )
    
    # Build the main layout with sidebar navigation
    app.layout = create_main_layout()
    
    # Register callbacks
    register_queue_callbacks(app)
    # TODO: Register other callbacks here
    
    return app

def run_dashboard():
    from pdf_parsing.config import settings
    app = create_app()
    app.run(host=settings.dash_host, port=settings.dash_port, debug=settings.dash_debug)
