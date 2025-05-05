import os, shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from app.agent import build_agent
from app.state import AgentState

app = FastAPI()
agent = build_agent()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/process_doc")
async def process_doc(file: UploadFile = File(...)):
    os.makedirs("temp", exist_ok=True)
    path = f"temp/{file.filename}"
    with open(path, "wb") as f: shutil.copyfileobj(file.file, f)

    state = AgentState(file_path=path)
    result = agent.invoke(state)
    os.remove(path)

    if not result.get("national_id"):
        return JSONResponse({"message": "No national ID found"}, status_code=400)
    if not result.get("customer_id"):
        return JSONResponse({"message": "No customer found"}, status_code=400)
    if not result.get("action"):
        return JSONResponse({"message": "No correct action"}, status_code=400)

    return {
    "national_id": result.get("national_id"),
    "customer_id": result.get("customer_id"),
    "action": result.get("action"),
    "outcome": result.get("outcome"),
    }

@app.get("/", response_class=HTMLResponse)
def home():
    return FileResponse("static/index.html")
