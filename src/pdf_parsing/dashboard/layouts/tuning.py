from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import dcc, html

def layout() -> dbc.Container:
    return dbc.Container(
        [
            html.H2("Prompt Tuning"),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Label("Document Type:"),
                            dcc.Dropdown(
                                id="tuning-doc-type",
                                options=[
                                    {"label": "Invoice", "value": "INVOICE"},
                                    {"label": "Receipt", "value": "RECEIPT"},
                                ],
                                placeholder="Select document type...",
                            ),
                        ],
                        width=6,
                    ),
                    dbc.Col(
                        [
                            html.Label("Test Document:"),
                            dcc.Dropdown(
                                id="tuning-test-doc",
                                placeholder="Select a PDF to test...",
                            ),
                        ],
                        width=6,
                    ),
                ],
                className="mb-4",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H4("System Prompt"),
                            dcc.Textarea(
                                id="tuning-prompt-area",
                                style={
                                    "width": "100%",
                                    "height": "400px",
                                    "fontFamily": "monospace",
                                },
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(dbc.Button("Test Prompt", id="btn-tuning-test", color="primary", className="mt-2 w-100")),
                                    dbc.Col(dbc.Button("Save Prompt", id="btn-tuning-save", color="success", className="mt-2 w-100")),
                                ]
                            ),
                        ],
                        width=6,
                    ),
                    dbc.Col(
                        [
                            html.H4("Test Results"),
                            html.Pre(
                                id="tuning-test-results",
                                style={
                                    "height": "400px",
                                    "overflowY": "scroll",
                                    "backgroundColor": "#f8f9fa",
                                    "padding": "10px",
                                    "border": "1px solid #dee2e6",
                                },
                            ),
                        ],
                        width=6,
                    ),
                ]
            ),
            html.Div(id="tuning-feedback", className="mt-3"),
        ],
        fluid=True,
    )
