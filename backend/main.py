import typer
from pathlib import Path
import logging
from db import init_db
# from parser import ingest_evidence
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
def add_evidence(case_path: Path, evidence_file: Path):
    """Add and ingest a new evidence file."""
    typer.echo(f"Stub: Ingesting {evidence_file} to {case_path}...")

@app.command()
def analyze(case_path: Path):
    """Run the AI analysis agent to generate findings and hypotheses."""
    typer.echo("Stub: Running AI analysis...")

@app.command()
def report(case_path: Path):
    """Generate Markdown and HTML reports from findings."""
    typer.echo(f"Stub: Generating report for {case_path}...")

if __name__ == "__main__":
    app()
