from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import dash_table, html

def layout() -> dbc.Container:
    return dbc.Container(
        [
            html.H2("Run History"),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(dbc.Card(dbc.CardBody([html.H5("Total Documents"), html.H2(id="hist-total-docs")]))),
                    dbc.Col(dbc.Card(dbc.CardBody([html.H5("Success Rate"), html.H2(id="hist-success-rate")]))),
                    dbc.Col(dbc.Card(dbc.CardBody([html.H5("Avg Confidence"), html.H2(id="hist-avg-conf")]))),
                    dbc.Col(dbc.Card(dbc.CardBody([html.H5("Avg Time (s)"), html.H2(id="hist-avg-time")]))),
                ],
                className="mb-4",
            ),
            dash_table.DataTable(
                id="history-data-table",
                columns=[
                    {"name": "Run ID", "id": "id"},
                    {"name": "Document Type", "id": "document_type"},
                    {"name": "Filename", "id": "source_file_name"},
                    {"name": "Status", "id": "status"},
                    {"name": "Confidence", "id": "confidence_score"},
                    {"name": "Processing Time", "id": "processing_time"},
                    {"name": "Timestamp", "id": "extracted_at"},
                ],
                data=[],
                filter_action="native",
                sort_action="native",
                page_size=20,
                style_table={"overflowX": "auto"},
                style_cell={"textAlign": "left"},
            ),
        ],
        fluid=True,
    )
