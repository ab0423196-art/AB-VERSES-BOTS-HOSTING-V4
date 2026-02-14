"""
Production-grade configuration management.
Centralized settings with validation and type safety.
"""

from typing import Optional
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # Application
    APP_NAME: str = "TelegramBotSaaS"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_PREFIX: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = Field(..., min_length=32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    DATABASE_URL: str
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    
    @property
    def REDIS_URL(self) -> str:
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    # Telegram
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_API_ID: int
    TELEGRAM_API_HASH: str
    
    # Docker
    DOCKER_BASE_URL: str = "unix://var/run/docker.sock"
    DOCKER_NETWORK: str = "telegram_bot_network"
    
    # Free Tier
    FREE_CPU_LIMIT: float = 0.5
    FREE_MEMORY_LIMIT: str = "512m"
    FREE_MAX_BOTS: int = 3
    FREE_MAX_DEPLOYMENTS_PER_DAY: int = 10
    
    # Premium Tier
    PREMIUM_CPU_LIMIT: float = 1.0
    PREMIUM_MEMORY_LIMIT: str = "1g"
    PREMIUM_MAX_BOTS: int = 15
    PREMIUM_MAX_DEPLOYMENTS_PER_DAY: int = 50
    
    # Business Tier
    BUSINESS_CPU_LIMIT: float = 2.0
    BUSINESS_MEMORY_LIMIT: str = "2g"
    BUSINESS_MAX_BOTS: int = 50
    BUSINESS_MAX_DEPLOYMENTS_PER_DAY: int = 200
    
    # Deployment
    DEPLOYMENT_TIMEOUT: int = 600
    MAX_UPLOAD_SIZE: int = 52428800
    TEMP_DIR: str = "/tmp/telegram-bot-deployments"
    CLONE_DIR: str = "/tmp/telegram-bot-clones"
    
    # Git
    GIT_CLONE_TIMEOUT: int = 300
    GIT_MAX_DEPTH: int = 1
    
    # Monitoring
    HEALTH_CHECK_INTERVAL: int = 60
    MAX_CRASH_COUNT: int = 5
    AUTO_RESTART: bool = True
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    BOT_LOG_RETENTION_DAYS: int = 7
    MAX_LOG_SIZE_MB: int = 100
    
    # Stripe
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_WEBHOOK_SECRET: Optional[str] = None
    STRIPE_PREMIUM_PRICE_ID: Optional[str] = None
    STRIPE_BUSINESS_PRICE_ID: Optional[str] = None
    
    # Razorpay
    RAZORPAY_KEY_ID: Optional[str] = None
    RAZORPAY_KEY_SECRET: Optional[str] = None
    
    # Admin
    ADMIN_USER_ID: int
    ADMIN_PASSWORD: str
    
    # Features
    ENABLE_ZIP_UPLOAD: bool = True
    ENABLE_GITHUB_DEPLOY: bool = True
    ENABLE_GIT_PULL: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def get_tier_limits(self, tier: str) -> dict:
        """Get resource limits for a specific tier."""
        limits = {
            "free": {
                "cpu": self.FREE_CPU_LIMIT,
                "memory": self.FREE_MEMORY_LIMIT,
                "max_bots": self.FREE_MAX_BOTS,
                "max_deployments": self.FREE_MAX_DEPLOYMENTS_PER_DAY,
            },
            "premium": {
                "cpu": self.PREMIUM_CPU_LIMIT,
                "memory": self.PREMIUM_MEMORY_LIMIT,
                "max_bots": self.PREMIUM_MAX_BOTS,
                "max_deployments": self.PREMIUM_MAX_DEPLOYMENTS_PER_DAY,
            },
            "business": {
                "cpu": self.BUSINESS_CPU_LIMIT,
                "memory": self.BUSINESS_MEMORY_LIMIT,
                "max_bots": self.BUSINESS_MAX_BOTS,
                "max_deployments": self.BUSINESS_MAX_DEPLOYMENTS_PER_DAY,
            },
        }
        return limits.get(tier.lower(), limits["free"])


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()


# Constants
class Tiers:
    FREE = "free"
    PREMIUM = "premium"
    BUSINESS = "business"
    ADMIN = "admin"


class BotStatus:
    PENDING = "pending"
    BUILDING = "building"
    RUNNING = "running"
    STOPPED = "stopped"
    FAILED = "failed"
    CRASHED = "crashed"
    UPDATING = "updating"


class DeploymentType:
    GITHUB = "github"
    ZIP = "zip"
    GIT_PULL = "git_pull"


class Language:
    PYTHON = "python"
    NODEJS = "nodejs"
    UNKNOWN = "unknown"
