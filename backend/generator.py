import csv
import json
from pathlib import Path
from datetime import datetime, timedelta
import random

def generate_demo_data(case_path: Path):
    """Generate synthetic CSV bank statements and fake EVTX JSON lines."""
    evidence_dir = case_path / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    
    bank_csv_path = evidence_dir / "bank_statements.csv"
    evtx_json_path = evidence_dir / "security_logs.jsonl"
    
    # 1. Generate Financial Data (CSV)
    # Date, Description, Amount, Counterparty, Balance
    start_date = datetime(2023, 10, 1)
    
    transactions = []
    balance = 50000.0
    
    # Add normal transactions
    for i in range(20):
        t_date = start_date + timedelta(days=i)
        amount = round(random.uniform(-500, 2000), 2)
        balance += amount
        transactions.append({
            "Date": t_date.strftime("%Y-%m-%d"),
            "Description": "Normal Transaction",
            "Amount": amount,
            "Counterparty": f"Entity_{random.randint(1,5)}",
            "Balance": round(balance, 2)
        })
        
    # Plant Anomaly 1: Structuring (Deposits just under 10k)
    structuring_date = start_date + timedelta(days=22)
    for i in range(3):
        amount = round(random.uniform(9000, 9900), 2)
        balance += amount
        transactions.append({
            "Date": (structuring_date + timedelta(hours=i)).strftime("%Y-%m-%d %H:%M:%S"),
            "Description": "Cash Deposit",
            "Amount": amount,
            "Counterparty": "Cash",
            "Balance": round(balance, 2)
        })
        
    # Plant Anomaly 2: Pass-through (money in, money out immediately)
    pass_date = start_date + timedelta(days=25)
    balance += 50000
    transactions.append({
        "Date": pass_date.strftime("%Y-%m-%d %H:%M:%S"),
        "Description": "Wire Transfer In",
        "Amount": 50000.0,
        "Counterparty": "ShellCorp LLC",
        "Balance": round(balance, 2)
    })
    balance -= 49500
    transactions.append({
        "Date": (pass_date + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
        "Description": "Wire Transfer Out",
        "Amount": -49500.0,
        "Counterparty": "Offshore Holdings",
        "Balance": round(balance, 2)
    })
    
    with open(bank_csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Date", "Description", "Amount", "Counterparty", "Balance"])
        writer.writeheader()
        for t in transactions:
            writer.writerow(t)
            
    # 2. Generate DFIR Data (Fake EVTX in JSONL)
    # We will simulate a suspicious login around the time of the structuring deposits
    evtx_events = [
        {
            "timestamp": (structuring_date - timedelta(hours=1)).isoformat(),
            "event_id": 4624,
            "description": "Logon",
            "user": "admin",
            "ip_address": "192.168.1.100"
        },
        {
            "timestamp": (structuring_date - timedelta(minutes=30)).isoformat(),
            "event_id": 4648,
            "description": "Logon using explicit credentials",
            "user": "admin",
            "target_server": "FINANCIAL_DB"
        }
    ]
    
    with open(evtx_json_path, 'w') as f:
        for event in evtx_events:
            f.write(json.dumps(event) + '\n')
            
    return bank_csv_path, evtx_json_path
