from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import dash_table, dcc, html

def layout() -> dbc.Container:
    return dbc.Container(
        [
            html.H2("Document Queue"),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Label("Document Type"),
                            dcc.Dropdown(
                                id="queue-doc-type-filter",
                                options=[
                                    {"label": "All", "value": "ALL"},
                                    {"label": "Invoice", "value": "INVOICE"},
                                    {"label": "Receipt", "value": "RECEIPT"},
                                ],
                                value="ALL",
                            ),
                        ],
                        width=3,
                    ),
                    dbc.Col(
                        [
                            html.Label("Status"),
                            dcc.Dropdown(
                                id="queue-status-filter",
                                options=[
                                    {"label": "All", "value": "ALL"},
                                    {"label": "Success", "value": "SUCCESS"},
                                    {"label": "Needs Review", "value": "NEEDS_REVIEW"},
                                    {"label": "Failed", "value": "FAILED"},
                                ],
                                value="ALL",
                            ),
                        ],
                        width=3,
                    ),
                    dbc.Col(
                        [
                            html.Label("Confidence Threshold"),
                            dcc.Slider(
                                id="queue-confidence-filter",
                                min=0,
                                max=1,
                                step=0.05,
                                value=0.0,
                                marks={0: "0", 0.5: "0.5", 1: "1"},
                            ),
                        ],
                        width=3,
                    ),
                    dbc.Col(
                        [
                            html.Label("Date Range"),
                            dcc.DatePickerRange(
                                id="queue-date-picker",
                                clearable=True,
                            ),
                        ],
                        width=3,
                    ),
                ],
                className="mb-4",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Button(
                            "Approve All Above Threshold",
                            id="btn-bulk-approve",
                            color="success",
                            className="me-2",
                        ),
                        width="auto",
                    ),
                    dbc.Col(
                        dbc.Button(
                            "Rerun Failed",
                            id="btn-rerun-failed",
                            color="warning",
                        ),
                        width="auto",
                    ),
                ],
                className="mb-3",
            ),
            dash_table.DataTable(
                id="queue-data-table",
                columns=[
                    {"name": "Filename", "id": "source_file_name"},
                    {"name": "Document Type", "id": "document_type"},
                    {"name": "Status", "id": "status"},
                    {"name": "Confidence", "id": "confidence_score"},
                    {"name": "Timestamp", "id": "extracted_at"},
                    {"name": "Actions", "id": "actions"},
                ],
                data=[],
                style_table={"overflowX": "auto"},
                style_cell={"textAlign": "left"},
                page_size=20,
            ),
            html.Div(id="queue-action-feedback", className="mt-3"),
        ],
        fluid=True,
    )
