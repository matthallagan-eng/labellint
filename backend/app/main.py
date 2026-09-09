from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings

app = FastAPI(
    title="LabelLint API",
    description="Dataset quality checks and annotation format conversion",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["ops"])
def health():
    return {"status": "ok"}