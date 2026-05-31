# 🚀 Production Deployment Checklist

> Your Django app now automatically applies production-grade security when `DEBUG=False`. Use this checklist before deploying.

---

## 🔐 **SECURITY SETTINGS (AUTOMATIC)**

When you set `DEBUG=False`, these security features are **automatically enabled**:

### ✅ HTTPS & Transport Layer
- [x] `SECURE_SSL_REDIRECT = True` → Auto-redirect HTTP to HTTPS
- [x] `SECURE_HSTS_SECONDS = 31536000` → Force HTTPS for 1 year
- [x] `SECURE_HSTS_INCLUDE_SUBDOMAINS = True` → Include all subdomains
- [x] `SECURE_HSTS_PRELOAD = True` → Added to browser HSTS preload list
- [x] `SECURE_PROXY_SSL_HEADER` → Trust X-Forwarded-Proto header (for reverse proxies)

### ✅ Cookie Security
- [x] `SESSION_COOKIE_SECURE = True` → HTTPS only
- [x] `CSRF_COOKIE_SECURE = True` → HTTPS only
- [x] `SESSION_COOKIE_HTTPONLY = True` → No JavaScript access
- [x] `CSRF_COOKIE_HTTPONLY = True` → No JavaScript access
- [x] `SESSION_COOKIE_SAMESITE = "Strict"` → No cross-site sending
- [x] `CSRF_COOKIE_SAMESITE = "Strict"` → Prevent CSRF attacks

### ✅ Content Security
- [x] `SECURE_BROWSER_XSS_FILTER = True` → Enable XSS protection
- [x] `X_CONTENT_TYPE_OPTIONS = "nosniff"` → Prevent MIME sniffing
- [x] `X_FRAME_OPTIONS = "DENY"` → Clickjacking protection
- [x] `SECURE_CONTENT_SECURITY_POLICY` → Comprehensive CSP headers

### ✅ Password Requirements
- [x] Minimum 12 characters (enforced in production)
- [x] Cannot be similar to username
- [x] Cannot be a common password
- [x] Cannot be purely numeric

### ✅ Static Files
- [x] WhiteNoise compression enabled
- [x] Manifest static file storage for cache busting

---

## 📋 **BEFORE DEPLOYING (Manual Steps)**

### 1. **Environment Variables** (REQUIRED)
```bash
# .env file or environment variable manager
DEBUG=False
SECRET_KEY=<generate with: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())">
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@host:port/dbname  # PostgreSQL recommended
REDIS_URL=redis://127.0.0.1:6379/1  # For caching

# Email settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

### 2. **Generate Secret Key** (DO THIS NOW!)
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
**⚠️ NEVER commit your real SECRET_KEY to git!**

### 3. **Database Setup**
```bash
# Use PostgreSQL in production (SQLite not recommended)
# Create database and run migrations
python manage.py migrate --settings=daily_essentials.settings
```

### 4. **Collect Static Files**
```bash
# Required for WhiteNoise to work
python manage.py collectstatic --noinput
```

### 5. **Install Production Dependencies**
```bash
pip install gunicorn whitenoise django-redis dj-database-url python-decouple
pip freeze > requirements.txt
```

### 6. **Create SSL Certificate**
- Use Let's Encrypt (free) via Certbot
- Or purchase from certificate authority
- Configure in your web server (Nginx, Apache)

### 7. **Web Server Setup** (Nginx + Gunicorn Example)
```bash
# Run with gunicorn
gunicorn daily_essentials.wsgi:application \
  --workers 4 \
  --worker-class sync \
  --timeout 120 \
  --bind 127.0.0.1:8000

# Configure Nginx reverse proxy
# Point to gunicorn, handle SSL, serve static files
```

### 8. **Database Backups**
```bash
# Set up automated PostgreSQL backups
pg_dump dbname > backup_$(date +%Y%m%d_%H%M%S).sql
```

### 9. **Logging Configuration**
```bash
# Enable application logging
# Monitor logs for errors and security issues
```

### 10. **Security Headers Verification**
Visit: https://securityheaders.com/
- Check all headers are being sent correctly
- Verify HSTS preload status

---

## 🔍 **TESTING BEFORE PRODUCTION**

### Verify Settings
```bash
# Check if DEBUG is False
python manage.py shell
>>> from django.conf import settings
>>> settings.DEBUG
False

# Check ALLOWED_HOSTS
>>> settings.ALLOWED_HOSTS
['yourdomain.com', 'www.yourdomain.com']
```

### Test HTTPS Redirect
```bash
curl -I http://yourdomain.com
# Should return 301 redirect to https://
```

### Test CSP Headers
```bash
curl -I https://yourdomain.com | grep -i content-security-policy
# Should show CSP policy
```

### Test HSTS Headers
```bash
curl -I https://yourdomain.com | grep -i strict-transport-security
# Should show HSTS max-age=31536000
```

---

## 📊 **MONITORING & MAINTENANCE**

### Weekly
- [ ] Check application error logs
- [ ] Monitor database size and performance
- [ ] Review failed login attempts

### Monthly
- [ ] Database backups verification
- [ ] SSL certificate expiration check (60+ days)
- [ ] Traffic analysis and performance metrics

### Quarterly
- [ ] Security dependency updates
- [ ] Django security updates
- [ ] SSL certificate renewal (if applicable)

### Annually
- [ ] Full security audit
- [ ] Penetration testing
- [ ] Update to latest Django LTS version

---

## 🚨 **PRODUCTION EMERGENCY PROCEDURES**

### If Database is Compromised
1. Stop all services
2. Restore from clean backup
3. Reset all user passwords
4. Review access logs
5. Update SECRET_KEY
6. Deploy updated settings

### If SSL Certificate Expires
1. Certbot auto-renewal should handle this
2. If manual, renew immediately
3. Restart web server with new certificate
4. Verify certificate is valid: `openssl s_client -connect yourdomain.com:443`

### If There's a DDoS Attack
1. Contact hosting provider
2. Enable DDoS protection
3. Consider WAF (Web Application Firewall)
4. Monitor server resources

---

## 📚 **HELPFUL COMMANDS**

```bash
# Check production settings are loaded
python manage.py diffsettings --settings=daily_essentials.settings

# Run security check
python manage.py check --deploy

# Collect static files
python manage.py collectstatic --noinput --clear

# Create superuser
python manage.py createsuperuser

# Check database migrations
python manage.py showmigrations

# Backup database
pg_dump -U username dbname > backup.sql

# Test SMTP email
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Subject', 'Message', 'from@example.com', ['to@example.com'])
```

---

## ✨ **QUICK START - DEPLOY TO PRODUCTION**

1. **Set environment variables:**
   ```bash
   export DEBUG=False
   export SECRET_KEY="<generated-key>"
   export ALLOWED_HOSTS="yourdomain.com,www.yourdomain.com"
   export DATABASE_URL="postgresql://..."
   ```

2. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Collect static files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Start Gunicorn:**
   ```bash
   gunicorn daily_essentials.wsgi:application --workers 4 --bind 127.0.0.1:8000
   ```

5. **Configure Nginx** (reverse proxy, SSL, serve static files)

6. **Enable SSL** (Let's Encrypt recommended)

7. **Monitor logs** and test all features

---

## 📖 **REFERENCES**

- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Mozilla Observatory](https://observatory.mozilla.org/)
- [Security Headers](https://securityheaders.com/)

---

**Last Updated:** May 2026
**Django Version:** 4.2+
**Status:** ✅ Ready for Production
