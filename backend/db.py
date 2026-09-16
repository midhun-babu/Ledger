import duckdb
from pathlib import Path

def init_db(db_path: Path):
    conn = duckdb.connect(str(db_path))
    # Create tables
    conn.execute("""
    CREATE TABLE IF NOT EXISTS timeline (
        id UUID PRIMARY KEY DEFAULT uuid(),
        timestamp TIMESTAMP,
        source VARCHAR,
        event_type VARCHAR,
        details JSON
    );
    
    CREATE TABLE IF NOT EXISTS hypotheses (
        id UUID PRIMARY KEY DEFAULT uuid(),
        description TEXT,
        status VARCHAR, -- 'Open', 'Confirmed', 'Refuted'
        confidence FLOAT,
        created_at TIMESTAMP DEFAULT current_timestamp
    );
    
    CREATE TABLE IF NOT EXISTS findings (
        id UUID PRIMARY KEY DEFAULT uuid(),
        description TEXT,
        evidence_refs JSON,
        hypothesis_id UUID,
        created_at TIMESTAMP DEFAULT current_timestamp
    );
    
    CREATE TABLE IF NOT EXISTS anomaly_flags (
        id UUID PRIMARY KEY DEFAULT uuid(),
        rule_name VARCHAR,
        description TEXT,
        evidence_refs JSON,
        severity VARCHAR,
        created_at TIMESTAMP DEFAULT current_timestamp
    );
    """)
    conn.close()
