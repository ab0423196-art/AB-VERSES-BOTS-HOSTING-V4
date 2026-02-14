# Telegram Bot SaaS Platform

A **production-grade SaaS platform** for deploying, managing, and monitoring Telegram bots. Built with FastAPI, PostgreSQL, Redis, Docker, and Pyrogram.

## 🚀 Features

### Core Functionality
- **GitHub Repository Deployment** - Deploy bots directly from GitHub repos
- **ZIP Upload Deployment** - Upload and deploy bot code as ZIP files
- **Git Pull & Auto-Deploy** - Pull latest changes and redeploy with one command
- **Multi-Language Support** - Python and Node.js bots
- **Container Isolation** - Each bot runs in its own Docker container
- **Resource Management** - CPU, memory, and disk quotas per tier

### Management & Monitoring
- **Real-time Monitoring** - CPU, RAM, and disk usage tracking
- **Live Logs** - Stream container logs in real-time
- **Health Checks** - Automatic health monitoring with auto-restart
- **Crash Detection** - Track and limit bot crashes
- **Uptime Tracking** - Monitor bot uptime and availability

### Security
- **JWT Authentication** - Secure API access
- **Tier-based Access Control** - Role-based permissions
- **Input Sanitization** - Prevent injection attacks
- **Token Leak Detection** - Automatically detect exposed secrets
- **Sandboxed Containers** - Isolated, non-privileged containers

### Billing & Tiers
- **Free Tier** - Limited resources for testing
- **Premium Tier** - Enhanced limits for serious users
- **Business Tier** - Maximum resources and priority support
- **Stripe Integration** - Ready for payment processing
- **Razorpay Support** - Indian payment gateway integration

### Advanced Features
- **Background Workers** - Celery-based task queue
- **Rate Limiting** - Prevent API abuse
- **Deployment Queue** - FIFO processing with retry logic
- **Log Rotation** - Automatic log cleanup and archiving
- **Metrics Collection** - Prometheus-compatible metrics

## 📁 Project Structure

```
telegram-bot-saas/
├── core/                       # Core configuration and infrastructure
│   ├── config.py              # Settings and environment variables
│   ├── database.py            # Database connection and session management
│   ├── security.py            # JWT, password hashing, validations
│   ├── redis_client.py        # Redis connection and cache operations
│   └── celery_app.py          # Celery task queue configuration
│
├── models/                     # SQLAlchemy database models
│   ├── user.py                # User model (tiers, limits, status)
│   ├── bot.py                 # Bot model (containers, resources)
│   ├── deployment.py          # Deployment history
│   ├── billing.py             # Transactions and subscriptions
│   └── bot_log.py             # Bot runtime logs
│
├── schemas/                    # Pydantic validation schemas
│   ├── user.py                # User request/response schemas
│   ├── bot.py                 # Bot schemas with validation
│   ├── deployment.py          # Deployment schemas
│   ├── auth.py                # Authentication schemas
│   └── billing.py             # Billing and payment schemas
│
├── services/                   # Business logic layer
│   ├── deployment_service.py  # Deployment orchestration
│   ├── container_service.py   # Container lifecycle management
│   ├── billing_service.py     # Payment processing
│   ├── monitoring_service.py  # Health checks and metrics
│   └── logging_service.py     # Log management
│
├── api/v1/endpoints/          # FastAPI API endpoints
│   ├── auth.py                # Authentication endpoints
│   ├── bots.py                # Bot management endpoints
│   ├── deploy.py              # Deployment endpoints
│   ├── logs.py                # Log retrieval endpoints
│   ├── billing.py             # Payment and subscription endpoints
│   ├── admin.py               # Admin-only endpoints
│   └── stats.py               # Statistics and analytics
│
├── telegram/                   # Telegram bot interface
│   ├── bot.py                 # Main Pyrogram bot
│   ├── handlers/              # Command and callback handlers
│   │   ├── start.py           # /start command
│   │   ├── deploy.py          # Deployment commands
│   │   ├── manage.py          # Bot management commands
│   │   ├── billing.py         # Billing and subscription commands
│   │   └── admin.py           # Admin commands
│   └── keyboards.py           # Inline keyboard builders
│
├── workers/                    # Celery background workers
│   ├── deployment_worker.py   # Deployment tasks
│   ├── monitoring_worker.py   # Health check tasks
│   ├── cleanup_worker.py      # Cleanup and maintenance tasks
│   └── billing_worker.py      # Billing and subscription tasks
│
├── utils/                      # Utility modules
│   ├── validators.py          # Input validation functions
│   ├── file_handler.py        # File upload and extraction
│   ├── git_handler.py         # Git operations (clone, pull)
│   └── docker_utils.py        # Docker SDK wrapper
│
├── middleware/                 # Custom middleware
│   ├── rate_limit.py          # Rate limiting middleware
│   └── error_handler.py       # Global error handling
│
├── docker/                     # Docker configuration
│   ├── Dockerfile             # Main application Dockerfile
│   ├── docker-compose.yml     # Multi-container setup
│   └── templates/             # Bot container templates
│       ├── python.Dockerfile  # Python bot template
│       └── nodejs.Dockerfile  # Node.js bot template
│
├── migrations/                 # Alembic database migrations
├── tests/                      # Unit and integration tests
├── scripts/                    # Utility scripts
├── logs/                       # Application logs
│
├── main.py                     # FastAPI application entry point
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
└── README.md                   # This file
```

## 🛠️ Tech Stack

- **Backend**: Python 3.11+, FastAPI
- **Database**: PostgreSQL (async with SQLAlchemy)
- **Cache/Queue**: Redis, Celery
- **Containers**: Docker SDK
- **Telegram**: Pyrogram
- **Payments**: Stripe, Razorpay
- **Monitoring**: Prometheus, structlog
- **Authentication**: JWT (python-jose)

## 📦 Installation

### Prerequisites
- Python 3.11+
- PostgreSQL 14+
- Redis 7+
- Docker 24+
- Telegram Bot Token (from @BotFather)

### Setup

1. **Clone Repository**
```bash
git clone https://github.com/yourusername/telegram-bot-saas.git
cd telegram-bot-saas
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Initialize Database**
```bash
alembic upgrade head
```

6. **Run Application**
```bash
# Start FastAPI
python main.py

# Start Telegram Bot (separate terminal)
python telegram/bot.py

# Start Celery Worker (separate terminal)
celery -A core.celery_app worker --loglevel=info

# Start Celery Beat (separate terminal)
celery -A core.celery_app beat --loglevel=info
```

## 🐳 Docker Deployment

```bash
docker-compose up -d
```

## 🔑 Environment Variables

Key environment variables (see `.env.example` for full list):

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash

# Security
SECRET_KEY=your-secret-key-min-32-chars

# Docker
DOCKER_BASE_URL=unix://var/run/docker.sock
```

## 💰 Tier Limits

| Feature | Free | Premium | Business |
|---------|------|---------|----------|
| Max Bots | 3 | 15 | 50 |
| CPU Limit | 0.5 | 1.0 | 2.0 |
| Memory Limit | 512MB | 1GB | 2GB |
| Deployments/Day | 10 | 50 | 200 |
| Priority Support | ❌ | ✅ | ✅ |

## 📚 API Documentation

Once running, access API docs at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Key Endpoints

#### Authentication
- `POST /api/v1/auth/login` - Admin login
- `POST /api/v1/auth/register` - User registration

#### Bots
- `GET /api/v1/bots` - List all user bots
- `GET /api/v1/bots/{bot_id}` - Get bot details
- `DELETE /api/v1/bots/{bot_id}` - Delete bot

#### Deployment
- `POST /api/v1/deploy/github` - Deploy from GitHub
- `POST /api/v1/deploy/zip` - Deploy from ZIP
- `POST /api/v1/deploy/git-pull` - Pull latest changes

#### Management
- `POST /api/v1/bots/{bot_id}/start` - Start bot
- `POST /api/v1/bots/{bot_id}/stop` - Stop bot
- `POST /api/v1/bots/{bot_id}/restart` - Restart bot

#### Logs
- `GET /api/v1/logs/{bot_id}` - Get bot logs
- `GET /api/v1/logs/{bot_id}/stream` - Stream logs

## 🤖 Telegram Bot Commands

- `/start` - Welcome message and registration
- `/mybots` - List your bots
- `/deploy` - Deploy new bot (GitHub or ZIP)
- `/stop {bot_id}` - Stop a bot
- `/start_bot {bot_id}` - Start a bot
- `/restart {bot_id}` - Restart a bot
- `/logs {bot_id}` - View bot logs
- `/stats {bot_id}` - View bot statistics
- `/gitpull {bot_id}` - Pull latest changes
- `/billing` - View subscription info
- `/upgrade` - Upgrade tier

## 🔐 Security Features

- **Input Validation** - All inputs sanitized
- **Token Detection** - Prevents accidental token exposure
- **Sandboxed Containers** - Isolated execution
- **Rate Limiting** - API abuse prevention
- **JWT Auth** - Secure API access
- **Password Hashing** - Bcrypt with salt
- **No Privileged Containers** - Security-first design

## 🎯 Deployment Types

### 1. GitHub Repository
```python
# Through API
POST /api/v1/deploy/github
{
  "name": "My Bot",
  "source_url": "https://github.com/user/repo",
  "git_branch": "main",
  "env_vars": {"BOT_TOKEN": "..."}
}
```

### 2. ZIP Upload
```python
# Through API
POST /api/v1/deploy/zip
Content-Type: multipart/form-data
file: bot.zip
name: "My Bot"
```

### 3. Git Pull (Update)
```python
POST /api/v1/deploy/git-pull
{
  "bot_id": "bot_abc123",
  "restart_after_pull": true
}
```

## 📊 Monitoring

- **Prometheus Metrics**: Available at `:9090/metrics`
- **Health Checks**: Automatic every 60 seconds
- **Resource Tracking**: CPU, RAM, disk per bot
- **Crash Detection**: Auto-restart with limits
- **Log Aggregation**: Centralized logging

## 🔧 Development

```bash
# Run tests
pytest

# Code formatting
black .

# Type checking
mypy .

# Linting
flake8 .
```

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions welcome! Please read CONTRIBUTING.md first.

## 📞 Support

- Email: support@yourdomain.com
- Telegram: @yoursupport
- Documentation: https://docs.yourdomain.com

## 🙏 Acknowledgments

Built with ❤️ using FastAPI, Pyrogram, and Docker.

---

**Note**: This is a production-grade platform. Ensure proper security configuration before deploying to production.
