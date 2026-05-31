# Development vs Production Settings Guide

## Quick Reference

### Running in Development

```bash
# Default (uses settings.py)
python manage.py runserver

# Or explicitly specify development settings
python manage.py runserver --settings=daily_essentials.settings
```

**Development Features:**
- ✅ Debug mode enabled
- ✅ Hot reload on file changes
- ✅ Detailed error pages
- ✅ No HTTPS enforcement
- ✅ SQLite database
- ✅ In-memory caching
- ✅ Easy to test
- ✅ Localhost only

**Environment File (.env):**
```
DEBUG=True
DJANGO_SETTINGS_MODULE=daily_essentials.settings
SECRET_KEY=dev-only-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost
```

---

### Running in Production

```bash
# Using Gunicorn
gunicorn daily_essentials.wsgi:application \
  --settings=daily_essentials.settings_production \
  --workers=4 \
  --bind=0.0.0.0:8000

# Or with systemd service
sudo systemctl start daily-essentials
```

**Production Features:**
- ✅ Debug mode disabled
- ✅ HTTPS enforced
- ✅ HSTS enabled
- ✅ CSP headers
- ✅ Secure cookies
- ✅ Static file compression
- ✅ Redis caching
- ✅ PostgreSQL database
- ✅ Error logging to file
- ✅ All security headers enabled

**Environment File (.env):**
```
DEBUG=False
DJANGO_SETTINGS_MODULE=daily_essentials.settings_production
SECRET_KEY=<generate-random-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@host:5432/db
REDIS_URL=redis://localhost:6379/1
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=app-password
```

---

## Settings File Comparison

| Setting | Development | Production |
|---------|-------------|------------|
| **Debug Mode** | True | False |
| **HTTPS Redirect** | No | Yes |
| **HSTS** | No | Yes (1 year) |
| **CSP Headers** | No | Yes |
| **Database** | SQLite | PostgreSQL |
| **Cache Backend** | Local Memory | Redis |
| **Static Files** | Django serves | Nginx serves + compression |
| **Session Backend** | Database | Redis Cache |
| **Logging** | Console | File + Console |
| **Error Tracking** | None | Sentry (optional) |
| **SECRET_KEY** | Default | Must generate |
| **Allowed Hosts** | localhost | Your domain |
| **Cookie Security** | No | Yes (secure, httponly) |
| **Worker Count** | 1 (dev server) | 4+ (gunicorn) |

---

## Security Comparison

### Development (settings.py)
```python
DEBUG = True
SECURE_SSL_REDIRECT = False  # HTTP allowed
SESSION_COOKIE_SECURE = False  # HTTP cookies
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0  # No HSTS
```

### Production (settings_production.py)
```python
DEBUG = False
SECURE_SSL_REDIRECT = True  # HTTPS only
SESSION_COOKIE_SECURE = True  # HTTPS cookies only
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Strict"
CSRF_COOKIE_SAMESITE = "Strict"

# HSTS enabled
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Content Security Policy
SECURE_CONTENT_SECURITY_POLICY = { ... }

# Other security headers
X_FRAME_OPTIONS = "DENY"
X_CONTENT_TYPE_OPTIONS = "nosniff"
SECURE_BROWSER_XSS_FILTER = True
```

---

## Deployment Steps Checklist

### 1. Before Deployment

- [ ] Test all features locally in development
- [ ] Run: `python manage.py check --deploy`
- [ ] Back up database
- [ ] Update settings_production.py if needed
- [ ] Generate new SECRET_KEY
- [ ] Prepare .env file for production

### 2. Database Preparation

```bash
# Create PostgreSQL database
sudo -u postgres psql
CREATE DATABASE daily_essentials;
CREATE USER de_user WITH PASSWORD 'strong-password';
GRANT ALL PRIVILEGES ON DATABASE daily_essentials TO de_user;

# Run migrations on production database
python manage.py migrate --settings=daily_essentials.settings_production

# Create superuser
python manage.py createsuperuser --settings=daily_essentials.settings_production

# Collect static files
python manage.py collectstatic --noinput --settings=daily_essentials.settings_production
```

### 3. Web Server Setup

```bash
# Copy code to production directory
git clone https://github.com/yourusername/daily-essentials.git /var/www/daily-essentials

# Install dependencies
cd /var/www/daily-essentials
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn psycopg2-binary dj-database-url django-redis whitenoise

# Copy .env file
cp .env.example .env
# Edit .env with production values
nano .env

# Make sure .env is secure
chmod 600 .env
```

### 4. SSL Certificate

```bash
# Using Let's Encrypt
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Certificates are in: /etc/letsencrypt/live/yourdomain.com/
```

### 5. Start Services

```bash
# Start Gunicorn service
sudo systemctl start daily-essentials
sudo systemctl enable daily-essentials

# Start Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Start Redis (if using)
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

### 6. Verify Deployment

```bash
# Check Gunicorn status
sudo systemctl status daily-essentials

# Check Nginx status
sudo systemctl status nginx

# Test website
curl -I https://yourdomain.com

# Check security headers
curl -I https://yourdomain.com | grep -i "strict-transport-security"

# Verify SSL certificate
openssl s_client -connect yourdomain.com:443
```

### 7. Post-Deployment

- [ ] Test all website features
- [ ] Verify SSL certificate (https://www.ssllabs.com)
- [ ] Test admin login
- [ ] Test email sending
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Update DNS records
- [ ] Enable HSTS preload (after 1 month)

---

## Common Commands by Environment

### Development

```bash
# Start server
python manage.py runserver

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test
```

### Production

```bash
# Start server
gunicorn daily_essentials.wsgi:application \
  --settings=daily_essentials.settings_production \
  --workers=4

# Or via systemd
sudo systemctl start daily-essentials

# Run migrations (after code updates)
python manage.py migrate --settings=daily_essentials.settings_production

# Collect static files (after code updates)
python manage.py collectstatic --noinput --settings=daily_essentials.settings_production

# Reload systemd service
sudo systemctl restart daily-essentials
```

---

## Security Checklist for Production

- [ ] DEBUG = False
- [ ] SECRET_KEY is unique and generated
- [ ] ALLOWED_HOSTS updated to your domain
- [ ] HTTPS/SSL certificate installed
- [ ] DATABASE_URL points to production database
- [ ] REDIS_URL configured for caching
- [ ] Email configuration correct
- [ ] SECURE_SSL_REDIRECT = True
- [ ] SESSION_COOKIE_SECURE = True
- [ ] CSRF_COOKIE_SECURE = True
- [ ] HSTS headers enabled
- [ ] Content Security Policy configured
- [ ] .env file has 600 permissions (chmod 600)
- [ ] Admin URL changed from default /admin/
- [ ] Backup strategy implemented
- [ ] Error tracking configured (Sentry)
- [ ] Logging configured
- [ ] Database backups automated
- [ ] SSL certificate auto-renewal configured
- [ ] Monitoring and alerting set up

---

## Troubleshooting

### Site returns 403 Forbidden
**Solution:** Check `ALLOWED_HOSTS` in settings or .env file

### SSL certificate error
**Solution:** Verify certificate path in Nginx config and check Let's Encrypt renewal

### Database connection refused
**Solution:** Verify DATABASE_URL in .env and PostgreSQL service is running

### Static files not loading
**Solution:** Run `python manage.py collectstatic` and verify Nginx configuration

### "CSRF token missing" errors
**Solution:** Ensure CSRF_COOKIE_SECURE is set correctly and domain matches ALLOWED_HOSTS

---

## References

- Settings file: [daily_essentials/settings_production.py](daily_essentials/settings_production.py)
- Deployment guide: [PRODUCTION_DEPLOYMENT_GUIDE.md](PRODUCTION_DEPLOYMENT_GUIDE.md)
- Django docs: https://docs.djangoproject.com/en/5.2/howto/deployment/
