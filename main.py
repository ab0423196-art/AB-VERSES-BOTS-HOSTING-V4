"""
Main FastAPI application entry point.
Production-grade SaaS platform for Telegram bot hosting.
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import structlog

from core.config import settings
from core.database import init_db, close_db
from core.redis_client import redis_client

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.processors.JSONRenderer() if settings.LOG_FORMAT == "json" else structlog.dev.ConsoleRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("application_starting", version=settings.APP_VERSION)
    
    try:
        # Initialize database
        await init_db()
        logger.info("database_initialized")
        
        # Connect to Redis
        await redis_client.connect()
        logger.info("redis_connected")
        
        logger.info("application_ready")
        yield
    
    finally:
        # Shutdown
        logger.info("application_shutting_down")
        
        # Close connections
        await redis_client.disconnect()
        await close_db()
        
        logger.info("application_stopped")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production SaaS Platform for Telegram Bot Hosting",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# Add middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure based on settings in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs" if settings.DEBUG else None,
    }


# Include API routers (to be created)
# from api.v1.endpoints import auth, bots, deploy, logs, billing, admin
# app.include_router(auth.router, prefix=f"{settings.API_PREFIX}/auth", tags=["auth"])
# app.include_router(bots.router, prefix=f"{settings.API_PREFIX}/bots", tags=["bots"])
# app.include_router(deploy.router, prefix=f"{settings.API_PREFIX}/deploy", tags=["deploy"])
# app.include_router(logs.router, prefix=f"{settings.API_PREFIX}/logs", tags=["logs"])
# app.include_router(billing.router, prefix=f"{settings.API_PREFIX}/billing", tags=["billing"])
# app.include_router(admin.router, prefix=f"{settings.API_PREFIX}/admin", tags=["admin"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
