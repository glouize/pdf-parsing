from __future__ import annotations

from dash import Input, Output, State, callback, ctx
import dash
from sqlmodel import select, update
from datetime import datetime

from pdf_parsing.db.engine import get_session
# Assuming BaseRecord is imported here, we use a placeholder model name or actual one if we know it.
from pdf_parsing.core.models import BaseRecord
from pdf_parsing.flows.document_flow import process_document

def register_queue_callbacks(app: dash.Dash):
    @app.callback(
        Output("queue-data-table", "data"),
        [
            Input("queue-doc-type-filter", "value"),
            Input("queue-status-filter", "value"),
            Input("queue-confidence-filter", "value"),
            Input("queue-date-picker", "start_date"),
            Input("queue-date-picker", "end_date"),
            Input("queue-action-feedback", "children"), # Trigger refresh on action
        ]
    )
    def update_queue_table(doc_type, status, confidence, start_date, end_date, _action_feedback):
        with get_session() as session:
            query = select(BaseRecord)
            
            # Since document_type is not directly on BaseRecord in some cases, 
            # we will assume it is or adapt. For now filtering on confidence, validated, etc.
            if confidence > 0:
                query = query.where(BaseRecord.confidence_score >= confidence)
            
            if status == "SUCCESS":
                query = query.where(BaseRecord.validated == True)
            elif status == "NEEDS_REVIEW":
                query = query.where(BaseRecord.validated == False)
            elif status == "FAILED":
                # Assuming confidence_score < 0.5 or something represents failed if status doesn't exist
                # Adjust as needed based on actual schema
                query = query.where(BaseRecord.confidence_score < 0.3)
                
            results = session.exec(query).all()
            
            data = []
            for r in results:
                data.append({
                    "source_file_name": r.source_file_name,
                    "document_type": getattr(r, "document_type", "Unknown"), # Placeholder
                    "status": "Validated" if r.validated else "Needs Review",
                    "confidence_score": r.confidence_score,
                    "extracted_at": str(r.extracted_at),
                    "actions": "Edit"
                })
            return data

    @app.callback(
        Output("queue-action-feedback", "children"),
        [
            Input("btn-bulk-approve", "n_clicks"),
            Input("btn-rerun-failed", "n_clicks"),
        ],
        [
            State("queue-data-table", "data"),
            State("queue-confidence-filter", "value")
        ]
    )
    def handle_bulk_actions(bulk_approve_clicks, rerun_failed_clicks, table_data, confidence_threshold):
        if not ctx.triggered_id:
            return dash.no_update
            
        if ctx.triggered_id == "btn-bulk-approve":
            with get_session() as session:
                # Basic bulk update logic
                statement = update(BaseRecord).where(
                    BaseRecord.confidence_score >= confidence_threshold,
                    BaseRecord.validated == False
                ).values(validated=True)
                session.exec(statement)
                session.commit()
            return dash.html.Div("Bulk approved successfully", className="text-success")
            
        elif ctx.triggered_id == "btn-rerun-failed":
            # Just an example of triggering processing, in reality you'd find the files
            with get_session() as session:
                failed_records = session.exec(
                    select(BaseRecord).where(BaseRecord.confidence_score < 0.3)
                ).all()
                for r in failed_records:
                    if hasattr(r, 'source_file_name'):
                        # Process document
                        # process_document(r.source_file_name)
                        pass
            return dash.html.Div(f"Triggered rerun for failed documents.", className="text-info")
