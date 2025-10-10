# Railway Deployment Guide for EscolaAPI

## Overview

This guide walks you through deploying EscolaAPI (Wellms Headless LMS) to Railway, including database setup and configuration.

## Architecture

EscolaAPI requires:
- **PostgreSQL Database** - Stores application data
- **Redis** (Optional) - For caching and queue management
- **Laravel Application** - The API service

## Phase 1: Railway Services Setup

### 1. Add PostgreSQL Database

In your Railway project dashboard:

1. Click **New** → **Database** → **Add PostgreSQL**
2. Railway automatically provisions and exposes connection variables

### 2. Add Redis Service (Optional but Recommended)

1. Click **New** → **Database** → **Add Redis**
2. Required for queue processing (Laravel Horizon) and caching

**Alternative:** Start without Redis by setting `DISABLE_HORIZON=true`

### 3. Deploy API Service

1. Connect your GitHub repository or use CLI
2. Railway will detect the Dockerfile and build automatically

## Phase 2: Environment Variable Configuration

In your Railway API service, go to **Variables** tab and configure:

### Database Connection

Use Railway's service reference syntax to auto-link:

```bash
DATABASE_URL=${{Postgres.DATABASE_URL}}
LARAVEL_DB_CONNECTION=pgsql
```

**OR** use individual variables:

```bash
LARAVEL_DB_HOST=${{Postgres.PGHOST}}
LARAVEL_DB_PORT=${{Postgres.PGPORT}}
LARAVEL_DB_DATABASE=${{Postgres.PGDATABASE}}
LARAVEL_DB_USERNAME=${{Postgres.PGUSER}}
LARAVEL_DB_PASSWORD=${{Postgres.PGPASSWORD}}
```

### Application Configuration

```bash
# App Settings
LARAVEL_APP_NAME=Wellms
LARAVEL_APP_ENV=production
LARAVEL_APP_DEBUG=false
LARAVEL_APP_URL=https://${{RAILWAY_PUBLIC_DOMAIN}}
LARAVEL_LOG_CHANNEL=stderr

# Security - IMPORTANT: Generate new key for production!
LARAVEL_APP_KEY=base64:pveos6JL8iCwO3MbzoyQpNx6TETMYuUpfZ18CDKl6Cw=
# Generate new key by running: php artisan key:generate
```

### Redis Configuration (If using Redis service)

```bash
LARAVEL_REDIS_HOST=${{Redis.REDIS_HOST}}
LARAVEL_REDIS_PASSWORD=${{Redis.REDIS_PASSWORD}}
LARAVEL_REDIS_PORT=${{Redis.REDIS_PORT}}
LARAVEL_CACHE_DRIVER=redis
LARAVEL_QUEUE_CONNECTION=redis
LARAVEL_SESSION_DRIVER=redis
```

### Storage Configuration

**Option A: Local Storage (Simple - for testing)**
```bash
LARAVEL_FILESYSTEM_DRIVER=local
```

**Option B: S3-Compatible Storage (Production)**
```bash
LARAVEL_FILESYSTEM_DRIVER=s3
LARAVEL_AWS_ACCESS_KEY_ID=your_key
LARAVEL_AWS_SECRET_ACCESS_KEY=your_secret
LARAVEL_AWS_DEFAULT_REGION=us-east-1
LARAVEL_AWS_BUCKET=your_bucket
LARAVEL_AWS_ENDPOINT=https://your-s3-endpoint.com
LARAVEL_AWS_URL=https://your-cdn-url.com
LARAVEL_AWS_USE_PATH_STYLE_ENDPOINT=false
```

### Mail Configuration (Optional)

```bash
LARAVEL_MAIL_DRIVER=smtp
LARAVEL_MAIL_HOST=smtp.your-provider.com
LARAVEL_MAIL_PORT=587
LARAVEL_MAIL_USERNAME=your_username
LARAVEL_MAIL_PASSWORD=your_password
LARAVEL_MAIL_ENCRYPTION=tls
LARAVEL_MAIL_FROM_ADDRESS=noreply@yourdomain.com
LARAVEL_MAIL_FROM_NAME="${LARAVEL_APP_NAME}"
```

### Service Control (Optional)

Disable specific services if not needed:

```bash
DISABLE_HORIZON=false      # Set to true to disable queue workers
DISABLE_SCHEDULER=false    # Set to true to disable cron jobs
DISABLE_DB_MIGRATE=false   # Set to true to skip auto-migrations
DISABLE_DB_SEED=false      # Set to true to skip seeding
```

### Initial User Configuration

```bash
LARAVEL_INITIAL_USER_PASSWORD=secret  # Default admin password
```

## Phase 3: Understanding the Init Process

When your container starts, `init.sh` automatically:

1. ✅ Creates necessary directories
2. ✅ Runs database migrations (`php artisan migrate`)
3. ✅ Generates Laravel Passport keys for OAuth
4. ✅ Seeds initial data (admin user, permissions)
5. ✅ Starts PHP-FPM, Laravel Horizon, and Scheduler via Supervisor

**This means your database will be automatically set up on first deployment!**

## Phase 4: Verify Deployment

### 1. Check Deployment Logs

In Railway dashboard:
- Click on your API service
- Go to **Deployments** tab
- Check logs for successful migration messages

### 2. Access API Documentation

Visit your Railway public domain:
```
https://your-app.railway.app/api/documentation
```

### 3. Test Login

Default credentials (created by seeder):
- **Email:** admin@escolalms.com
- **Password:** secret (or value from `LARAVEL_INITIAL_USER_PASSWORD`)

## Phase 5: Post-Deployment Security

### Generate New APP_KEY (Critical for Production!)

1. In Railway CLI or via Railway shell:
```bash
php artisan key:generate --show
```

2. Copy the output and update `LARAVEL_APP_KEY` in Railway variables
3. Redeploy

### Update Admin Password

After first login, immediately change the default admin password!

## Troubleshooting

### Connection Refused Errors

**Symptom:** `SQLSTATE[HY000] [2002] Connection refused`

**Solutions:**
- Ensure Postgres service is created in Railway
- Verify `DATABASE_URL` or individual DB variables are set
- Check that variables use `${{Postgres.VARIABLE}}` syntax
- Ensure services are in the same Railway project

### Horizon/Queue Failures

**Symptom:** Laravel Horizon keeps restarting

**Solutions:**
- If not using queues yet, set `DISABLE_HORIZON=true`
- Ensure Redis service is created and linked
- Verify Redis variables are set correctly

### Migration Fails

**Symptom:** Migrations fail during startup

**Solutions:**
- Check database credentials
- Ensure database service is fully started (Railway shows "Active")
- Review logs for specific migration errors
- Temporarily set `DISABLE_DB_MIGRATE=true` to skip migrations and debug

### Storage/Upload Issues

**Symptom:** File uploads fail

**Solutions:**
- For testing: Use `LARAVEL_FILESYSTEM_DRIVER=local`
- For production: Configure S3-compatible storage
- Ensure Railway persistent volume is configured if using local storage

## Advanced Configuration

### Persistent Storage

If using `FILESYSTEM_DRIVER=local`, add a Railway volume:

1. In Railway service settings → **Volumes**
2. Add volume mounted at `/var/www/html/storage/app`

### Custom Domain

1. In Railway service → **Settings** → **Domains**
2. Add your custom domain
3. Update `LARAVEL_APP_URL` to match

### Scaling

Railway supports:
- **Vertical scaling:** Increase CPU/RAM in service settings
- **Horizontal scaling:** Add replicas (requires shared storage/sessions)

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | - | Full Postgres connection string |
| `LARAVEL_APP_KEY` | Yes | - | Laravel encryption key (base64) |
| `LARAVEL_APP_URL` | Yes | - | Public URL of your API |
| `LARAVEL_DB_CONNECTION` | Yes | `pgsql` | Database driver |
| `LARAVEL_REDIS_HOST` | If using Redis | - | Redis host |
| `LARAVEL_FILESYSTEM_DRIVER` | No | `local` | Storage driver (local/s3) |
| `DISABLE_HORIZON` | No | `false` | Disable queue workers |
| `DISABLE_SCHEDULER` | No | `false` | Disable cron jobs |

## Support & Documentation

- **EscolaAPI Docs:** https://docs.wellms.io/
- **API Documentation:** https://api-docs.wellms.io
- **Railway Docs:** https://docs.railway.com/
- **GitHub:** https://github.com/EscolaLMS/API

## Quick Start Checklist

- [ ] Create Railway project
- [ ] Add PostgreSQL database service
- [ ] Add Redis service (optional)
- [ ] Deploy API service from GitHub
- [ ] Configure environment variables (minimum: DATABASE_URL, APP_KEY, APP_URL)
- [ ] Check deployment logs for successful migration
- [ ] Access API documentation at your Railway domain
- [ ] Login with default credentials
- [ ] Change admin password
- [ ] Generate new APP_KEY for production
- [ ] Configure storage (S3 for production)
- [ ] Set up custom domain (optional)

---

**Ready to deploy!** 🚀
