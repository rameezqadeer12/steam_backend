from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

# -------------------------
# FastAPI App
# -------------------------
app = FastAPI(title="EduTech Render Proxy API")

# -------------------------
# CORS CONFIG (VERY IMPORTANT)
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://edu-tech-xgg.vercel.app",   # your Vercel frontend
        "http://localhost:3000",             # local dev
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# ENV VARIABLES
# -------------------------
RENDER_API_KEY = os.getenv("RENDER_API_KEY", "punjab123")
RENDER_URL = os.getenv(
    "RENDER_URL",
    "https://punjabtextbook-production.up.railway.app/ask"
)

# -------------------------
# HEALTH CHECK
# -------------------------
@app.get("/")
def health():
    return {"status": "EduTech API running on Render"}

# -------------------------
# MAIN PROXY ENDPOINT
# -------------------------
@app.post("/ask")
def ask(payload: dict, x_api_key: str = Header(None)):
    # 🔐 API Key check
    if x_api_key != RENDER_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    try:
        response = requests.post(
            RENDER_URL,
            json=payload,
            headers={
                "Content-Type": "application/json",
                "x-api-key": RENDER_API_KEY
            },
            timeout=30
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Forward response safely
    try:
        return response.json()
    except Exception:
        return {
            "status": response.status_code,
            "text": response.text
        }
