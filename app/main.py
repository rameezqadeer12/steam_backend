from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database.database import engine, Base

# -------------------------
# APP LIFESPAN
# -------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
    yield
    # Shutdown
    print("⏹️ Shutting down")

# -------------------------
# FASTAPI APP
# -------------------------
app = FastAPI(
    title="EduLLMs API",
    description="Educational LLM Chat Backend",
    version="1.0.0",
    lifespan=lifespan
)

# -------------------------
# ✅ CORS (FINAL & CORRECT)
# -------------------------
# ❌ app = FastAPI(...)   ← THIS LINE REMOVED (ERROR FIX)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://edu-tech-xgg.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routers AFTER cors
from app.api.endpoints import router as api_router
from app.api.websocket import router as ws_router

app.include_router(api_router, prefix="/api")
app.include_router(ws_router, prefix="/ws")

# -------------------------
# BASIC ENDPOINTS
# -------------------------
@app.get("/")
async def root():
    return {"message": "EduLLMs API is running 🚀"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}
