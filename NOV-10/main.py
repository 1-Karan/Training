import os
import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Dict

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "meta-llama/llama-3.1-8b-instruct"

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
log = logging.getLogger("svc")

app = FastAPI(title="FastAPI Backend")

# --- CORS (Streamlit runs on another port) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

# --- Simple logging middleware ---
class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        log.info(f"{request.method} {request.url.path}")
        resp = await call_next(request)
        log.info(f"-> {resp.status_code}")
        return resp

app.add_middleware(LogMiddleware)

# ----- Schemas -----
class AddReq(BaseModel):
    a: float
    b: float

class ReverseReq(BaseModel):
    text: str

class QueryReq(BaseModel):
    query: str

# ----- Endpoints -----

@app.post("/api/add")
def add_numbers(payload: AddReq) -> Dict[str, float]:
    return {"sum": payload.a + payload.b}

@app.get("/api/date")
def todays_date() -> Dict[str, str]:
    ist = datetime.now(ZoneInfo("Asia/Kolkata"))
    return {"today_ist": ist.strftime("%Y-%m-%d"), "time_ist": ist.strftime("%H:%M:%S")}

@app.post("/api/reverse")
def reverse_word(payload: ReverseReq) -> Dict[str, str]:
    return {"reversed": payload.text[::-1]}

@app.post("/api/generate")
def generate_answer(payload: QueryReq) -> Dict[str, str]:
    query = payload.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    if not API_KEY:
        raise HTTPException(status_code=500, detail="Missing OPENROUTER_API_KEY in .env")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "http://localhost:8501",  # or your deployed frontend URL
        "X-Title": "FastAPI-Streamlit-Demo",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    body = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query},
        ],
    }

    try:
        r = requests.post(OPENROUTER_URL, headers=headers, json=body, timeout=30)
        log.info(f"Status: {r.status_code}")
        log.info(f"Raw response: {r.text[:300]}")  # debug line

        r.raise_for_status()
        data = r.json()
        answer = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        ).strip()
        if not answer:
            answer = "No content from model. Try rephrasing or switch model."
        return {"response": answer}
    except requests.Timeout:
        raise HTTPException(status_code=504, detail="LLM request timed out.")
    except requests.RequestException as e:
        log.error(f"Upstream error: {e}")
        raise HTTPException(status_code=502, detail="OpenRouter upstream error.")
    except Exception as e:
        log.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
