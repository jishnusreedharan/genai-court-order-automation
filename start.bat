@echo off
echo Installing dependencies...

call venv\Scripts\activate

python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Starting FastAPI server...
uvicorn app.main:app --reload --port 8000
