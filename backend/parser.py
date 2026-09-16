import duckdb
import csv
import json
from pathlib import Path
from datetime import datetime
import uuid

def ingest_evidence(evidence_file: Path, db_path: Path, parsed_dir: Path):
    """Parse evidence and load into DuckDB timeline table."""
    conn = duckdb.connect(str(db_path))
    
    if evidence_file.suffix.lower() == '.csv':
        # Assume it's a financial bank statement based on our schema
        with open(evidence_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    # Support both Date and DateTime formats from generator
                    dt = datetime.strptime(row['Date'], "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    dt = datetime.strptime(row['Date'], "%Y-%m-%d")
                    
                details = json.dumps({
                    "Amount": float(row['Amount']),
                    "Counterparty": row['Counterparty'],
                    "Balance": float(row['Balance'])
                })
                conn.execute("""
                    INSERT INTO timeline (timestamp, source, event_type, details)
                    VALUES (?, ?, ?, ?)
                """, (dt, 'bank_statement.csv', 'financial_transaction', details))
                
    elif evidence_file.suffix.lower() == '.jsonl':
        # Fake EVTX JSONL
        with open(evidence_file, 'r', encoding='utf-8') as f:
            for line in f:
                event = json.loads(line)
                dt = datetime.fromisoformat(event['timestamp'])
                details = json.dumps(event)
                conn.execute("""
                    INSERT INTO timeline (timestamp, source, event_type, details)
                    VALUES (?, ?, ?, ?)
                """, (dt, 'security_logs.jsonl', 'evtx_logon', details))
                
    conn.close()
