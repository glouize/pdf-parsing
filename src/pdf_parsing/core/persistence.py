from __future__ import annotations

import datetime
import structlog
from sqlmodel import Session, SQLModel

from pdf_parsing.db.engine import get_session
from pdf_parsing.core.models import BaseRecord

logger = structlog.get_logger(__name__)

def persist_records(
    records: list[SQLModel],
    source_document_id: str,
    source_file_name: str,
    confidence_score: float | None = None,
    session: Session | None = None,
) -> list[int]:
    """Persist parsed records to the database."""
    logger.info("Persisting records", count=len(records), document_id=source_document_id)
    
    def _do_persist(db_session: Session) -> list[int]:
        now = datetime.datetime.now(datetime.timezone.utc)
        
        # Simple algorithm to separate parents and children based on relationships
        # This checks if a record has a field pointing to another record in the list
        parents = []
        children = []
        
        for record in records:
            if isinstance(record, BaseRecord):
                record.source_document_id = source_document_id
                record.source_file_name = source_file_name
                record.confidence_score = confidence_score
                record.extracted_at = now
            
            # Simple heuristic: if any attribute is an instance of a record in the list, it's a child
            is_child = False
            for attr_name in dir(record):
                if not attr_name.startswith("_"):
                    try:
                        val = getattr(record, attr_name)
                        if val in records and val is not record:
                            is_child = True
                            break
                    except Exception:
                        pass
            
            if is_child:
                children.append(record)
            else:
                parents.append(record)
                
        # Insert parents first
        for parent in parents:
            db_session.add(parent)
        db_session.flush()
        
        # Then children
        for child in children:
            db_session.add(child)
            
        db_session.commit()
        
        inserted_ids = []
        for record in records:
            db_session.refresh(record)
            if hasattr(record, "id") and record.id is not None:
                inserted_ids.append(record.id)
                
        return inserted_ids

    if session is not None:
        return _do_persist(session)
    else:
        with get_session() as db_session:
            return _do_persist(db_session)
