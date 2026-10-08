from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from pdf_parsing.config import settings

def init_db() -> None:
    from pdf_parsing.db.engine import init_db as initialize
    initialize()
    print("Database initialized.")

def main() -> None:
    parser = argparse.ArgumentParser(prog='pdf-parsing')
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('list-types', help='List registered document types')

    new_type_parser = subparsers.add_parser('new-type', help='Scaffold a new document type')
    new_type_parser.add_argument('name', help='Name for the new document type')

    run_parser = subparsers.add_parser('run', help='Process a single PDF')
    run_parser.add_argument('document_type', help='Document type name')
    run_parser.add_argument('pdf_path', help='Path to PDF file')

    subparsers.add_parser('init-db', help='Initialize database tables')

    args = parser.parse_args()

    if args.command == 'list-types':
        from pdf_parsing.core.registry import registry
        types = registry.list_types()
        if not types:
            print("No document types registered.")
        for t in types:
            print(f"- {t}")

    elif args.command == 'new-type':
        name = args.name
        template_dir = settings.document_types_dir / "_template"
        target_dir = settings.document_types_dir / name
        
        if target_dir.exists():
            print(f"Error: Document type '{name}' already exists.")
            sys.exit(1)
            
        shutil.copytree(template_dir, target_dir)
        
        # Replace placeholders
        pascal_name = "".join(word.capitalize() for word in name.split("_"))
        
        config_path = target_dir / "config.yaml"
        if config_path.exists():
            content = config_path.read_text(encoding="utf-8")
            content = content.replace("__DOCUMENT_TYPE_NAME__", name)
            content = content.replace("__DOCUMENT_TYPE_NAME_PASCAL__", pascal_name)
            config_path.write_text(content, encoding="utf-8")
            
        print(f"Created new document type '{name}' at {target_dir}")

    elif args.command == 'run':
        from pdf_parsing.flows.document_flow import process_document
        print(f"Starting pipeline for '{args.document_type}' on '{args.pdf_path}'...")
        result = process_document(pdf_path=args.pdf_path, document_type=args.document_type)
        if result.success:
            print(f"Success! Inserted {len(result.record_ids)} records. Processing time: {result.processing_time_seconds:.2f}s")
            print(f"Confidence score: {result.parse_result.confidence_score if result.parse_result else 'N/A'}")
        else:
            print(f"Failed: {result.error}")

    elif args.command == 'init-db':
        init_db()
        
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
