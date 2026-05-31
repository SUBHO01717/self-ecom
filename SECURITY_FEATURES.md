# Security Features: Development vs Production

## 🔓 Development (settings.py)

### Security Settings
```python
DEBUG = True                                    # Shows error details
SECURE_SSL_REDIRECT = False                     # No HTTPS requirement
SESSION_COOKIE_SECURE = False                   # HTTP cookies allowed
CSRF_COOKIE_SECURE = False                      # HTTP CSRF cookies allowed
```

### Enabled Security Features
✅ CSRF Protection (basic)
✅ Session Security (basic)
✅ Admin interface protection

### Disabled Security Features
❌ HTTPS enforcement
❌ HSTS headers
❌ Secure cookies
❌ Content Security Policy
❌ XSS protection headers
❌ Clickjacking protection
❌ MIME type sniffing protection

### Best For
- Local development
- Testing
- Learning Django

### ⚠️ DO NOT USE IN PRODUCTION

---

## 🔐 Production (settings_production.py)

### Core Security Settings
```python
DEBUG = False                                   # Hide sensitive information
SECURE_SSL_REDIRECT = True                      # Force HTTPS
SESSION_COOKIE_SECURE = True                    # HTTPS only
CSRF_COOKIE_SECURE = True                       # HTTPS only
```

### All Enabled Security Features

#### 1. HTTPS & Transport Security
```python
✅ SECURE_SSL_REDIRECT = True
   → Automatically redirect HTTP to HTTPS
   
✅ SECURE_HSTS_SECONDS = 31536000 (1 year)
   → Forces browser to use HTTPS
   
✅ SECURE_HSTS_INCLUDE_SUBDOMAINS = True
   → Applies to all subdomains
   
✅ SECURE_HSTS_PRELOAD = True
   → Included in browser HSTS preload list
```

#### 2. Cookie Security
```python
✅ SESSION_COOKIE_SECURE = True
   → Session cookie sent only over HTTPS
   
✅ CSRF_COOKIE_SECURE = True
   → CSRF token sent only over HTTPS
   
✅ SESSION_COOKIE_HTTPONLY = True
   → JavaScript cannot access session cookie
   
✅ CSRF_COOKIE_HTTPONLY = True
   → JavaScript cannot access CSRF token
   
✅ SESSION_COOKIE_SAMESITE = "Strict"
   → Prevents cross-site session theft
   
✅ CSRF_COOKIE_SAMESITE = "Strict"
   → Prevents cross-site CSRF attacks
```

#### 3. Content Security Policy (CSP)
```python
✅ SECURE_CONTENT_SECURITY_POLICY = {
    "default-src": ("'self'",),
    "script-src": ("'self'", "'unsafe-inline'", 
                   "https://cdn.tailwindcss.com",
                   "https://www.googletagmanager.com"),
    "style-src": ("'self'", "'unsafe-inline'",
                  "https://cdn.tailwindcss.com"),
    "img-src": ("'self'", "data:", "https:", "blob:"),
    "font-src": ("'self'", "data:", "https:"),
    "connect-src": ("'self'",
                    "https://www.googletagmanager.com",
                    "https://connect.facebook.net"),
    "frame-ancestors": ("'self'",),
    "base-uri": ("'self'",),
    "form-action": ("'self'",),
}
   → Prevents XSS, code injection, and framing attacks
```

#### 4. Frame & Type Protection
```python
✅ X_FRAME_OPTIONS = "DENY"
   → Prevents clickjacking attacks (page can't be framed)
   
✅ X_CONTENT_TYPE_OPTIONS = "nosniff"
   → Prevents MIME type sniffing attacks
```

#### 5. XSS Protection
```python
✅ SECURE_BROWSER_XSS_FILTER = True
   → Browser blocks detected XSS attacks
```

#### 6. Database Security
```python
✅ Atomic Transactions
   → All or nothing database operations
   
✅ Connection Health Checks
   → Automatic reconnection on DB failure
```

#### 7. Session Security
```python
✅ SESSION_ENGINE = "django.contrib.sessions.backends.cache"
   → Sessions stored in Redis (fast & secure)
   
✅ SESSION_CACHE_ALIAS = "default"
   → Uses Redis backend
```

#### 8. Static Files
```python
✅ STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
   → Automatic minification and gzip compression
   → Cache-busting with content hashing
   → Enables efficient caching (1 year expiry)
```

#### 9. Logging & Monitoring
```python
✅ File-based logging to /var/log/gunicorn/
✅ Rotating file handler (10MB max files)
✅ Keeps 10 backup log files
✅ Security events logged at WARNING level
```

#### 10. Email Security
```python
✅ SMTP with TLS encryption
✅ App-specific passwords (for Gmail)
✅ Authentication required
```

---

## Security Comparison Table

| Feature | Development | Production |
|---------|-------------|-----------|
| **Debug Mode** | ✅ ON | ❌ OFF |
| **HTTPS Redirect** | ❌ No | ✅ Yes |
| **HSTS Header** | ❌ No | ✅ 1 year |
| **Secure Cookies** | ❌ No | ✅ Yes |
| **HTTPOnly Cookies** | ❌ No | ✅ Yes |
| **SameSite Cookies** | ❌ No | ✅ Strict |
| **CSP Header** | ❌ No | ✅ Yes |
| **X-Frame-Options** | ❌ No | ✅ DENY |
| **X-Content-Type-Options** | ❌ No | ✅ nosniff |
| **XSS Filter** | ❌ No | ✅ Yes |
| **Database** | SQLite | PostgreSQL |
| **Cache** | Memory | Redis |
| **Session Storage** | Database | Redis Cache |
| **Static Compression** | ❌ No | ✅ Yes |
| **Error Tracking** | ❌ No | ✅ Optional (Sentry) |
| **Log to File** | ❌ No | ✅ Yes |

---

## Request Flow Comparison

### Development (settings.py)
```
User Browser
    ↓ HTTP/HTTPS (both allowed)
    ↓
Django Dev Server (runserver)
    ↓
SQLite Database
    ↓
Response (full debug info if error)
```

### Production (settings_production.py)
```
User Browser (HTTP)
    ↓
Nginx (reverse proxy)
    ↓ Redirect to HTTPS
    ↓
Nginx (SSL termination)
    ↓ X-Forwarded-Proto: https
    ↓
Gunicorn (multiple workers)
    ↓ All security headers added
    ↓
Redis Cache (check if cached)
    ↓
PostgreSQL Database
    ↓
Response (no debug info, minimal error details)
    ↓ Secure headers added
    ↓
User Browser (with CSP, HSTS, etc.)
```

---

## Attack Prevention

### Development (Limited Protection)
```
Attack Type | Protected
-----------|----------
CSRF | ✅ Basic
XSS | ❌ No
Clickjacking | ❌ No
MITM | ❌ No
Session Hijacking | ❌ No
Cookie Theft | ❌ No
MIME Sniffing | ❌ No
```

### Production (Full Protection)
```
Attack Type | Protected | How
-----------|-----------|-----
CSRF | ✅ Full | CSRF token + SameSite cookie
XSS | ✅ Full | CSP + XSS filter + HTTPOnly
Clickjacking | ✅ Full | X-Frame-Options: DENY
MITM | ✅ Full | HTTPS + HSTS preload
Session Hijacking | ✅ Full | Secure HTTPOnly SameSite
Cookie Theft | ✅ Full | Secure HTTPOnly HTTPS only
MIME Sniffing | ✅ Full | X-Content-Type-Options
Brute Force | ✅ Partial | Rate limiting (optional)
SQL Injection | ✅ Full | Django ORM
```

---

## Environment Variables Impact

### Development
```bash
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
# Most security features are disabled
```

### Production
```bash
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
# All security features are enabled
# HTTPS required
# CSP enforced
# Cookies secured
# Errors logged securely
```

---

## Switching Between Environments

### To Use Development Settings
```bash
export DJANGO_SETTINGS_MODULE=daily_essentials.settings
# or
python manage.py runserver --settings=daily_essentials.settings
```

### To Use Production Settings
```bash
export DJANGO_SETTINGS_MODULE=daily_essentials.settings_production
# or
gunicorn daily_essentials.wsgi:application \
  --settings=daily_essentials.settings_production
```

---

## OWASP Top 10 Coverage

| OWASP Top 10 | Risk | Production Protection |
|--------|---------|----------------------|
| **A01: Broken Access Control** | High | ✅ Session security + HTTPOnly cookies |
| **A02: Cryptographic Failures** | High | ✅ HTTPS + TLS + Secure cookies |
| **A03: Injection** | High | ✅ Django ORM parameterization |
| **A04: Insecure Design** | High | ✅ CSRF tokens + Django forms |
| **A05: Security Misconfiguration** | High | ✅ All security headers configured |
| **A06: Vulnerable Components** | High | ✅ Regularly updated dependencies |
| **A07: Authentication Failures** | High | ✅ Session security + password validators |
| **A08: Software & Data Integrity** | Medium | ✅ Secure headers + HSTS |
| **A09: Logging & Monitoring** | Medium | ✅ File logging configured |
| **A10: SSRF** | Medium | ✅ Content-Security-Policy |

---

## SSL/TLS Configuration

### Production (settings_production.py)
```python
✅ SECURE_SSL_REDIRECT = True
   → Forces all traffic through HTTPS
   
✅ SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
   → Trusts proxy headers from Nginx
   
✅ TLS 1.2 and 1.3 (in Nginx)
   → Modern encryption protocols
   
✅ Certificate from Let's Encrypt
   → Free, trusted certificate authority
```

---

## Recommended Production Checklist

- [ ] All security features in settings_production.py enabled
- [ ] SSL certificate installed from Let's Encrypt
- [ ] HTTPS redirect working
- [ ] HSTS headers verified
- [ ] CSP headers verified
- [ ] Secure cookies enabled
- [ ] Debug mode OFF
- [ ] Secret key generated
- [ ] ALLOWED_HOSTS updated
- [ ] PostgreSQL database running
- [ ] Redis cache running
- [ ] Nginx reverse proxy configured
- [ ] Gunicorn service running
- [ ] Automated backups configured
- [ ] Error logging to file
- [ ] Monitoring enabled
- [ ] SSL certificate auto-renewal set up

---

## Key Takeaways

### Development (settings.py)
⚡ Fast & Easy  
🐛 Debug-friendly  
📝 Shows errors  
⚠️ Not secure  

### Production (settings_production.py)  
🔐 Maximum security  
🚀 Performant  
📊 Comprehensive logging  
✅ Production-ready  

**Never use development settings in production!**

