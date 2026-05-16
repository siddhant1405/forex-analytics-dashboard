"""
Currency Hub backend application entry point.
"""

import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import conversion, currencies, performance, trends

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Currency Hub API",
    description="Backend API for the Currency Hub forex analytics dashboard. Provides real-time conversion, historical trends with statistical indicators, and global currency performance tracking.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Allow local development origins by default and extend them in production
# via the CORS_ALLOW_ORIGINS environment variable.
cors_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

extra_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ALLOW_ORIGINS", "").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[*cors_origins, *extra_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(currencies.router)
app.include_router(conversion.router)
app.include_router(trends.router)
app.include_router(performance.router)


@app.get("/", tags=["health"])
async def root():
    return {
        "service": "Currency Hub API",
        "version": "1.0.0",
        "status": "healthy",
        "docs": "/docs",
    }


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}
