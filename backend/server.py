from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import duckdb
from pydantic import BaseModel
import os

app = FastAPI()

# Allow CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CaseRequest(BaseModel):
    case_path: str

@app.get("/api/timeline")
def get_timeline(case_path: str):
    db_path = os.path.join(case_path, "database", "case.duckdb")
    if not os.path.exists(db_path):
        return {"error": "Database not found"}
    
    conn = duckdb.connect(db_path)
    # Get last 100 timeline events for UI
    results = conn.execute("SELECT * FROM timeline ORDER BY timestamp DESC LIMIT 100").fetchall()
    columns = [desc[0] for desc in conn.description]
    conn.close()
    
    return [dict(zip(columns, row)) for row in results]

@app.get("/api/hypotheses")
def get_hypotheses(case_path: str):
    db_path = os.path.join(case_path, "database", "case.duckdb")
    if not os.path.exists(db_path):
        return {"error": "Database not found"}
        
    conn = duckdb.connect(db_path)
    results = conn.execute("SELECT * FROM hypotheses ORDER BY created_at DESC").fetchall()
    columns = [desc[0] for desc in conn.description]
    conn.close()
    
    return [dict(zip(columns, row)) for row in results]

@app.get("/api/findings")
def get_findings(case_path: str):
    db_path = os.path.join(case_path, "database", "case.duckdb")
    if not os.path.exists(db_path):
        return {"error": "Database not found"}
        
    conn = duckdb.connect(db_path)
    results = conn.execute("SELECT * FROM findings ORDER BY created_at DESC").fetchall()
    columns = [desc[0] for desc in conn.description]
    conn.close()
    
    return [dict(zip(columns, row)) for row in results]
