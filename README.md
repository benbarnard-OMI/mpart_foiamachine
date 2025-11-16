# MPART FOIA Machine

A customized version of foiamachine for MPART

## Quick Start with Docker

The easiest way to deploy this application is using Docker Compose:

1. **Copy environment file**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and configure your settings.

2. **Start all services**:
   ```bash
   docker-compose up -d --build
   ```

3. **Create a superuser**:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

4. **Access the application**:
   - Web: http://localhost:8000
   - Admin: http://localhost:8000/admin

For detailed Docker deployment instructions, see [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md).

For an overview of the Docker architecture, see [DOCKER_PLAN.md](DOCKER_PLAN.md).

## Manual Installation

For manual installation without Docker, see the project documentation.

## Services

- **Web**: Django application (Gunicorn)
- **Celery**: Background task worker
- **Celery Beat**: Scheduled task scheduler
- **PostgreSQL**: Database
- **Redis**: Message broker and cache
