Write-Host "Starting Backend FastAPI server..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; .\venv\Scripts\activate; uvicorn server:app --reload --port 8000"

Write-Host "Starting Frontend Vite server..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host "Services starting. Backend on 8000, Frontend on 5173 (usually)."
