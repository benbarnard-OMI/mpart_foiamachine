# Docker Deployment Guide

This guide explains how to deploy the MPART FOIA Machine using Docker and Docker Compose.

## Prerequisites

- Docker Engine 20.10 or later
- Docker Compose 2.0 or later

## Quick Start

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create environment file**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and update the values, especially:
   - `SECRET_KEY`: Generate a new secret key for Django
   - `POSTGRES_PASSWORD`: Set a strong password
   - `ALLOWED_HOSTS`: Add your domain name(s)

3. **Build and start services**:
   ```bash
   docker-compose up -d --build
   ```

4. **Create a superuser** (first time only):
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

5. **Access the application**:
   - Web application: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

## Services

The Docker Compose setup includes the following services:

- **web**: Django application server (Gunicorn)
- **celery**: Celery worker for background tasks
- **celery-beat**: Celery beat scheduler for periodic tasks
- **db**: PostgreSQL database
- **redis**: Redis server for Celery broker and cache

## Common Commands

### Start services
```bash
docker-compose up -d
```

### Stop services
```bash
docker-compose stop
```

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f celery
```

### Run Django management commands
```bash
docker-compose exec web python manage.py <command>
```

### Run migrations
```bash
docker-compose exec web python manage.py migrate
```

### Create superuser
```bash
docker-compose exec web python manage.py createsuperuser
```

### Access Django shell
```bash
docker-compose exec web python manage.py shell
```

### Restart a specific service
```bash
docker-compose restart web
docker-compose restart celery
```

### Rebuild after code changes
```bash
docker-compose up -d --build
```

## Environment Variables

Key environment variables (configured in `.env`):

- **SECRET_KEY**: Django secret key (required)
- **DEBUG**: Set to `False` in production
- **ALLOWED_HOSTS**: Comma-separated list of allowed hostnames
- **DATABASE_URL**: PostgreSQL connection string
- **CELERY_BROKER_URL**: Redis connection for Celery
- **EMAIL_***: Email configuration
- **OPENAI_API_KEY**: For AI agent features

See `.env.example` for all available options.

## Production Deployment

For production deployment:

1. **Update `.env` file**:
   - Set `DEBUG=False`
   - Set `ALLOWED_HOSTS` to your domain
   - Use strong passwords
   - Configure proper email backend
   - Set up AWS S3 for media/static files (optional)

2. **Use a reverse proxy** (recommended):
   - Nginx or Apache in front of the Docker containers
   - Configure SSL/TLS certificates

3. **Set up backups**:
   - Regular database backups
   - Volume backups for media files

4. **Monitor resources**:
   - Set appropriate resource limits in `docker-compose.yml`
   - Monitor logs and performance

## Troubleshooting

### Database connection errors
- Ensure the database service is healthy: `docker-compose ps`
- Check database logs: `docker-compose logs db`
- Verify `DATABASE_URL` in `.env`

### Static files not loading
- Run collectstatic: `docker-compose exec web python manage.py collectstatic --noinput`
- Check static volume: `docker-compose exec web ls -la /app/staticfiles`

### Celery tasks not running
- Check Celery logs: `docker-compose logs celery`
- Verify Redis connection: `docker-compose exec redis redis-cli ping`
- Check `CELERY_BROKER_URL` in `.env`

### Port conflicts
- Change `PORT` in `.env` if 8000 is already in use
- Update port mapping in `docker-compose.yml` if needed

## Data Persistence

Data is persisted in Docker volumes:
- `postgres_data`: Database data
- `static_volume`: Collected static files
- `media_volume`: User-uploaded media files

To backup:
```bash
docker-compose exec db pg_dump -U foiamachine foiamachine > backup.sql
```

To restore:
```bash
docker-compose exec -T db psql -U foiamachine foiamachine < backup.sql
```

## Scaling

To scale services:

```bash
# Scale web workers
docker-compose up -d --scale web=3

# Scale celery workers
docker-compose up -d --scale celery=4
```

Note: Update `docker-compose.yml` to configure load balancing if scaling web services.

## Maintenance

### Update dependencies
1. Update `requirements.txt`
2. Rebuild: `docker-compose build --no-cache`
3. Restart: `docker-compose up -d`

### Database migrations
Migrations run automatically on container start. To run manually:
```bash
docker-compose exec web python manage.py migrate
```

### Clear cache
```bash
docker-compose exec redis redis-cli FLUSHALL
```

## Security Notes

- Never commit `.env` file to version control
- Use strong passwords in production
- Keep Docker images updated
- Regularly review and update dependencies
- Use secrets management for sensitive data in production
