import typer
from pathlib import Path
import logging
from db import init_db
from parser import ingest_evidence
from generator import generate_demo_data
from anomalies import detect_anomalies
# from agent import run_analysis
# from report import generate_report

app = typer.Typer(help="Forensic AI Assistant CLI")

@app.command()
def init(case_path: Path):
    """Initialize a new forensic case folder structure."""
    case_path.mkdir(parents=True, exist_ok=True)
    (case_path / "evidence").mkdir(exist_ok=True)
    (case_path / "parsed").mkdir(exist_ok=True)
    (case_path / "database").mkdir(exist_ok=True)
    (case_path / "reports").mkdir(exist_ok=True)
    (case_path / "logs").mkdir(exist_ok=True)
    
    # Initialize DB
    init_db(case_path / "database" / "case.duckdb")
    
    # Setup logging
    logging.basicConfig(filename=case_path / "logs" / "assistant.log", level=logging.INFO)
    logging.info(f"Initialized case at {case_path}")
    typer.echo(f"Case initialized at {case_path}")

@app.command()
def generate_demo(case_path: Path):
    """Generate synthetic DFIR and Financial evidence for a demo case."""
    if not (case_path / "database" / "case.duckdb").exists():
        init(case_path)
    
    typer.echo("Generating synthetic evidence...")
    bank_csv, evtx_json = generate_demo_data(case_path)
    
    typer.echo("Ingesting evidence...")
    add_evidence(case_path, bank_csv)
    add_evidence(case_path, evtx_json)
    
    typer.echo("Demo case generated successfully.")

@app.command()
def add_evidence(case_path: Path, evidence_file: Path):
    """Add and ingest a new evidence file."""
    db_path = case_path / "database" / "case.duckdb"
    if not db_path.exists():
        typer.echo("Error: DB not found. Run init first.")
        raise typer.Exit(1)
        
    typer.echo(f"Ingesting {evidence_file}...")
    ingest_evidence(evidence_file, db_path, case_path / "parsed")
    typer.echo("Evidence ingested successfully.")

@app.command()
def analyze(case_path: Path):
    """Run deterministic anomaly checks, then AI analysis."""
    db_path = case_path / "database" / "case.duckdb"
    if not db_path.exists():
        typer.echo("Error: DB not found.")
        raise typer.Exit(1)
        
    typer.echo("Running deterministic anomaly rules...")
    detect_anomalies(db_path)
    typer.echo("Anomalies generated.")
    
    typer.echo("Stub: Running AI analysis loop (hypothesis -> verify -> findings)...")
    # run_analysis(db_path)
    typer.echo("Analysis complete.")

@app.command()
def report(case_path: Path):
    """Generate Markdown and HTML reports from findings."""
    typer.echo(f"Stub: Generating structured report (Exec Summary, DFIR, Financial, Evidence Index) for {case_path}...")

if __name__ == "__main__":
    app()
