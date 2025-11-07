import os
import json
import logging
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
log = logging.getLogger("qa_service")

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing OPENROUTER_API_KEY in .env")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "meta-llama/llama-3.1-8b-instruct"

DB_PATH = Path("data/qa_history.db")
DB_PATH.parent.mkdir(exist_ok=True)

def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL
            );
            """
        )
        conn.commit()

def record_history(question: str, answer: str) -> None:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO history (timestamp, question, answer) VALUES (?, ?, ?)",
                (datetime.utcnow().isoformat(), question, answer),
            )
            conn.commit()
        log.debug("History saved.")
    except Exception as exc:
        log.warning(f"Unable to save history: {exc}")

init_db()

app = FastAPI(title="OpenRouter Chat Service")
templates = Jinja2Templates(directory=".")

class Question(BaseModel):
    query: str

def query_openrouter(prompt: str) -> str:
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    }
    try:
        resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data: Dict = resp.json()
        reply = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        if not reply:
            reply = "No content received from model. Try rephrasing your question."
        return reply
    except requests.Timeout:
        raise HTTPException(status_code=504, detail="Request to OpenRouter timed out.")
    except requests.RequestException as exc:
        log.error(f"HTTP error: {exc}")
        raise HTTPException(status_code=502, detail="Failed to contact OpenRouter.")
    except Exception as exc:
        log.exception("Unexpected error during OpenRouter call.")
        raise HTTPException(status_code=500, detail=str(exc))

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate_from_form(query: str = Form(...)):
    cleaned = query.strip()
    if not cleaned:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    log.info("Processing query via form submission.")
    answer = query_openrouter(cleaned)
    record_history(cleaned, answer)
    return {"response": answer}

@app.post("/api/generate", response_model=Dict[str, str])
async def generate_from_json(prompt: Question):
    cleaned = prompt.query.strip()
    if not cleaned:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    log.info("Processing query via JSON API.")
    answer = query_openrouter(cleaned)
    record_history(cleaned, answer)
    return {"response": answer}
