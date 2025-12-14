from fastapi import FastAPI, File, UploadFile, Header, HTTPException, Form
from datetime import datetime
from .storage import upload_to_landing
import json
import os

app = FastAPI()

API_KEYS = json.loads(os.getenv("API_KEYS", "{}"))

@app.post("/ingest")
async def ingest(file: UploadFile = File(...), dataset: str = Form(...),
                 x_api_key: str = Header(...)):
    
    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    source = API_KEYS[x_api_key]
    print(f"source: {source}")

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV allowed")

    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"{dataset}_{ts}.csv"
    print(f"filename: {filename}")

    content = await file.read()
    path = upload_to_landing(partner=source, dataset=dataset, filename=file.filename,
                             data=file.file)
    print(f"path received: {path}")

    return {"status": "success", "path": f"landing/{path}/{dataset}/{filename}"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "api-ingestion-service",
        "environment": "kubernetes"
    }