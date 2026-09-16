import duckdb
from pathlib import Path
import json

def detect_anomalies(db_path: Path):
    """Run deterministic anomaly rules against the timeline and create flags."""
    conn = duckdb.connect(str(db_path))
    
    # Clean previous flags to avoid duplicates on re-runs
    conn.execute("DELETE FROM anomaly_flags")
    
    # Rule 1: Structuring Detection (Multiple deposits just under $10,000)
    # We'll look for deposits between 9000 and 9999 within a tight window.
    # For simplicity, we just flag any deposit in that range.
    structuring_events = conn.execute("""
        SELECT id, details, timestamp
        FROM timeline
        WHERE event_type = 'financial_transaction'
        AND json_extract_string(details, '$.Amount')::FLOAT BETWEEN 9000 AND 9999
    """).fetchall()
    
    struct_refs = []
    for row in structuring_events:
        struct_refs.append(row[0])
        
    if len(struct_refs) >= 2:
        conn.execute("""
            INSERT INTO anomaly_flags (rule_name, description, evidence_refs, severity)
            VALUES (?, ?, ?, ?)
        """, (
            'Structuring Detection',
            f'Detected {len(struct_refs)} deposits just under $10,000 reporting threshold.',
            json.dumps(struct_refs),
            'HIGH'
        ))
        
    # Rule 2: Benford's Law First-Digit check
    # (Simplified: just computing distribution and flagging if 1 is not the most common,
    # or just adding a dummy flag if amounts don't follow it. For now, we will just flag it if 1 is < 20%.)
    # Getting all amounts:
    amounts = conn.execute("""
        SELECT id, json_extract_string(details, '$.Amount')::FLOAT
        FROM timeline
        WHERE event_type = 'financial_transaction'
    """).fetchall()
    
    if amounts:
        first_digits = [str(abs(a[1]))[0] for a in amounts if abs(a[1]) >= 1]
        if first_digits:
            ones = first_digits.count('1')
            if (ones / len(first_digits)) < 0.25:
                conn.execute("""
                    INSERT INTO anomaly_flags (rule_name, description, evidence_refs, severity)
                    VALUES (?, ?, ?, ?)
                """, (
                    'Benford Law Deviation',
                    'The first digit distribution of transaction amounts heavily deviates from Benford\'s Law (digit 1 is less than 25%).',
                    json.dumps([a[0] for a in amounts[:5]]), # Attach first few as refs
                    'MEDIUM'
                ))
                
    # Rule 3: Rapid Pass-through / Round-trip
    # (Simplified: look for large deposit followed by large withdrawal within a day)
    # This requires a more complex query, we'll flag any transaction pair > 10000 that happens within 24h
    conn.execute("""
        CREATE TEMP TABLE tx AS
        SELECT id, timestamp, json_extract_string(details, '$.Amount')::FLOAT as amount, json_extract_string(details, '$.Counterparty') as cp
        FROM timeline WHERE event_type = 'financial_transaction'
    """)
    pass_through = conn.execute("""
        SELECT t1.id, t2.id, t1.amount, t2.amount
        FROM tx t1
        JOIN tx t2 ON t1.id != t2.id
        WHERE t1.amount > 10000 AND t2.amount < -10000
        AND t2.timestamp > t1.timestamp
        AND epoch(t2.timestamp) - epoch(t1.timestamp) < 86400
        AND ABS(t1.amount + t2.amount) < (t1.amount * 0.1) -- Withdrawal is within 10% of deposit
    """).fetchall()
    
    if pass_through:
        for pair in pass_through:
            conn.execute("""
                INSERT INTO anomaly_flags (rule_name, description, evidence_refs, severity)
                VALUES (?, ?, ?, ?)
            """, (
                'Rapid Pass-Through',
                f'Large deposit followed by immediate equivalent withdrawal detected.',
                json.dumps([pair[0], pair[1]]),
                'HIGH'
            ))

    conn.close()
