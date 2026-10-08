from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import dcc, html

def layout() -> dbc.Container:
    return dbc.Container(
        [
            html.H2("Validation"),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Label("Select Document to Review:"),
                            dcc.Dropdown(
                                id="validation-doc-selector",
                                placeholder="Select a document...",
                            ),
                        ],
                        width=6,
                    ),
                    dbc.Col(
                        [
                            html.Div(id="validation-confidence-indicator", className="mt-4")
                        ],
                        width=6,
                        className="text-end",
                    ),
                ],
                className="mb-4",
            ),
            dbc.Row(
                [
                    # Left panel: source document info
                    dbc.Col(
                        [
                            html.H4("Source Document"),
                            html.Div(id="validation-source-filename", className="mb-2 fw-bold"),
                            html.Pre(
                                id="validation-extracted-text",
                                style={
                                    "maxHeight": "600px",
                                    "overflowY": "scroll",
                                    "backgroundColor": "#f8f9fa",
                                    "padding": "10px",
                                    "border": "1px solid #dee2e6",
                                },
                            ),
                        ],
                        width=6,
                    ),
                    # Right panel: parsed data
                    dbc.Col(
                        [
                            html.H4("Extracted Data"),
                            html.Div(
                                id="validation-form-fields",
                                style={
                                    "maxHeight": "600px",
                                    "overflowY": "scroll",
                                    "padding": "10px",
                                },
                            ),
                            html.Hr(),
                            dbc.Row(
                                [
                                    dbc.Col(dbc.Button("Approve", id="btn-val-approve", color="success", className="w-100")),
                                    dbc.Col(dbc.Button("Edit & Save", id="btn-val-save", color="primary", className="w-100")),
                                    dbc.Col(dbc.Button("Rerun", id="btn-val-rerun", color="warning", className="w-100")),
                                ]
                            ),
                            html.Div(id="validation-action-feedback", className="mt-3"),
                        ],
                        width=6,
                    ),
                ]
            ),
        ],
        fluid=True,
    )
