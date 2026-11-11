from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.endpoints.chat import router as chat_router
from app.api.v1.endpoints.document import router as document_router
from app.api.v1.endpoints.health import router as health_router
from app.core.config import settings
from app.core.exception_handler import register_exception_handlers
from app.database.init_db import create_tables
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting BSWAN AI API...")

    # Create database tables
    create_tables()

    yield

    print("🛑 Shutting down BSWAN AI API...")


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan=lifespan,
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
# Register Global Exception Handlers
register_exception_handlers(app)

# -------------------------
# API Routes
# -------------------------

# Health
app.include_router(
    health_router,
    prefix="/api/v1",
    tags=["Health"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chat
app.include_router(
    chat_router,
    prefix="/api/v1/chat",
    tags=["Chat"]
)

# Documents
app.include_router(
    document_router,
    prefix="/api/v1",
    tags=["Documents"]
)


@app.get("/")
def root():
    return {
        "application": settings.APP_NAME,
        "version": "1.0.0",
        "status": "Running",
        "docs": "/docs"
    }