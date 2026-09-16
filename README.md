# Forensic AI Assistant

The **Forensic AI Assistant** is a local, fully-offline Windows forensic investigation tool powered by AI. It is designed to assist forensic analysts in processing raw evidence, constructing a chronological timeline, autonomously forming and testing hypotheses against the data, and generating comprehensive investigation reports. 

## Key Features

- **Fully Offline Processing:** Designed to run 100% locally. No case data ever leaves your machine, ensuring complete data privacy and operational security.
- **Automated Evidence Ingestion:** Processes standard Windows forensic artifacts including EVTX (Event Logs), MFT (Master File Table), Prefetch files, and Registry hives into a normalized timeline.
- **High-Performance Storage:** Uses DuckDB for extremely fast querying of massive sets of timeline data.
- **AI-Powered Reasoning:** Connects to any local OpenAI-compatible API server (e.g., LM Studio, Ollama). The AI agent acts as a co-investigator, analyzing the timeline, formulating hypotheses, verifying them against the evidence database, and documenting concrete findings.
- **Modern Web Dashboard:** Provides a beautiful, dark-themed, interactive web UI built with React to easily view timelines, track the AI's logic and hypotheses, and read final reports.

## Project Structure

The project is split into two primary components:

### Backend (Python)
The brains of the operation. It includes a Typer-based CLI for managing the forensic investigation lifecycle and a FastAPI server for exposing the data.

- **CLI Usage:**
  - `python backend/main.py init <case_path>`: Initializes a new case directory with the necessary subfolders (evidence, parsed, database, reports, logs) and sets up the DuckDB database.
  - `python backend/main.py add-evidence <case_path> <evidence_file>`: Parses a raw evidence file and inserts the normalized timeline events into the case database.
  - `python backend/main.py analyze <case_path>`: Kicks off the AI reasoning loop to analyze the timeline and generate hypotheses and findings.
  - `python backend/main.py report <case_path>`: Instructs the AI to compile all findings into a structured Markdown and HTML report.

### Frontend (React & Vite)
A dynamic, responsive dashboard designed to provide a premium user experience while interacting with case data.

- **Dashboard:** At-a-glance metrics of parsed events and active hypotheses.
- **Timeline View:** An interactive list of all timeline events loaded from the DuckDB instance via the FastAPI backend.
- **AI Insights (WIP):** Watch the AI’s thought process as it logs hypotheses and confirmed findings in real-time.
- **Final Report (WIP):** Review the finalized, AI-generated investigation report directly in the browser.

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js & npm
- A local AI model server (e.g., LM Studio or Ollama) running locally and exposing an OpenAI-compatible API.

### Running the Application

You can launch both the Python backend API and the React frontend simultaneously using the included PowerShell script:

```powershell
.\start.ps1
```

Once running:
- The backend API will be available at `http://localhost:8000`
- The frontend Web UI will be available at `http://localhost:5173`

Open your browser to the frontend URL to begin visualizing your forensic case data.
