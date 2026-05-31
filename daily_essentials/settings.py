from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================================
# ENVIRONMENT & DEBUG
# ============================================================================
DEBUG = config("DEBUG", default=True, cast=bool)

# CRITICAL: In production, set SECRET_KEY via environment variable
if DEBUG:
    SECRET_KEY = config("SECRET_KEY", default="dev-only-secret-key")
else:
    SECRET_KEY = config("SECRET_KEY", default=None)
    if SECRET_KEY is None:
        raise ValueError(
            "SECRET_KEY environment variable is required in production. "
            "Generate with: python -c \"from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())\""
        )

# Production: Provide ALLOWED_HOSTS as comma-separated (e.g., "example.com,www.example.com")
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="127.0.0.1,localhost", cast=Csv())

if not DEBUG and not ALLOWED_HOSTS:
    raise ValueError("ALLOWED_HOSTS environment variable is required in production")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_ckeditor_5",
    "core",
    "settings_manager",
    "categories",
    "products",
    "campaigns",
    "customers",
    "orders",
    "cart",

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "daily_essentials.urls"
CKEDITOR_5_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "settings_manager.context_processors.site_settings",
                "cart.context_processors.cart_summary",
            ],
        },
    }
]

WSGI_APPLICATION = "daily_essentials.wsgi.application"

# ============================================================================
# DATABASE - Development vs Production
# ============================================================================
# Production: Set DATABASE_URL environment variable for PostgreSQL
DATABASE_URL = config("DATABASE_URL", default=None)

if DATABASE_URL:
    # Production: Use PostgreSQL via dj-database-url
    try:
        import dj_database_url
        DATABASES = {
            "default": dj_database_url.config(
                default=DATABASE_URL,
                conn_max_age=600,
                conn_health_checks=True,
            )
        }
    except ImportError:
        raise ImportError("dj-database-url is required for PostgreSQL support. Install with: pip install dj-database-url")
else:
    # Development: Use SQLite
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
            "ATOMIC_REQUESTS": not DEBUG,  # Atomic requests in production
        }
    }

# ============================================================================
# PASSWORD VALIDATION
# ============================================================================
if DEBUG:
    AUTH_PASSWORD_VALIDATORS = [
        {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    ]
else:
    # Production: Enforce stronger password requirements
    AUTH_PASSWORD_VALIDATORS = [
        {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 12}},
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    ]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Dhaka"
USE_I18N = True
USE_TZ = True

# ============================================================================
# STATIC AND MEDIA FILES
# ============================================================================
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Production: Use WhiteNoise for efficient static file serving
if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
else:
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_URL = "customers:login"
LOGIN_REDIRECT_URL = "customers:dashboard"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST", default="")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="Daily Essentials <noreply@example.com>")


CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": {
            "items": [
                "heading", "|",
                "bold", "italic", "underline", "strikethrough", "|",
                "fontSize", "fontFamily", "fontColor", "fontBackgroundColor", "|",
                "link", "insertImage", "insertTable", "mediaEmbed", "|",
                "bulletedList", "numberedList", "todoList", "|",
                "outdent", "indent", "|",
                "alignment", "|",
                "blockQuote", "codeBlock", "horizontalLine", "|",
                "specialCharacters", "removeFormat", "|",
                "undo", "redo", "|",
                "sourceEditing"
            ]
        },
        "image": {
            "toolbar": [
                "imageTextAlternative",
                "imageStyle:inline",
                "imageStyle:block",
                "imageStyle:side",
                "toggleImageCaption",
            ]
        },
        "table": {
            "contentToolbar": [
                "tableColumn",
                "tableRow",
                "mergeTableCells",
                "tableProperties",
                "tableCellProperties",
            ]
        },
        "language": "en",
    }
}

# ============================================================================
# SECURITY HEADERS & HTTPS (ENVIRONMENT-BASED)
# ============================================================================

# Always enabled security features
SECURE_BROWSER_XSS_FILTER = False  # Disabled to prevent conflicts with modern JS frameworks
X_CONTENT_TYPE_OPTIONS = "nosniff"
X_FRAME_OPTIONS = "DENY"

# Content Security Policy - same for dev & production
SECURE_CONTENT_SECURITY_POLICY = {
    "default-src": ("'self'",),
    "script-src": (
        "'self'",
        "'unsafe-inline'",
        "https://cdn.tailwindcss.com",
        "https://www.googletagmanager.com",
        "https://www.google-analytics.com",
        "https://connect.facebook.net",
    ),
    "style-src": (
        "'self'",
        "'unsafe-inline'",
        "https://cdn.tailwindcss.com",
    ),
    "img-src": ("'self'", "data:", "https:", "blob:"),
    "font-src": ("'self'", "data:", "https:"),
    "connect-src": (
        "'self'",
        "https://www.googletagmanager.com",
        "https://www.google-analytics.com",
        "https://connect.facebook.net",
    ),
    "frame-ancestors": ("'self'",),
    "base-uri": ("'self'",),
    "form-action": ("'self'",),
}

# Production security settings
if not DEBUG:
    # HTTPS/HSTS Configuration (PRODUCTION ONLY)
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True  # Only after full testing
    
    # Cookie Security
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Strict"
    CSRF_COOKIE_SAMESITE = "Strict"
    
    # Production cache (Redis)
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": config("REDIS_URL", default="redis://127.0.0.1:6379/1"),
            "KEY_PREFIX": "daily_essentials",
            "TIMEOUT": 300,  # 5 minutes default
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
        }
    }
else:
    # Development: Insecure cookies for local testing
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = False
    CSRF_COOKIE_HTTPONLY = False
    SESSION_COOKIE_SAMESITE = "Lax"
    CSRF_COOKIE_SAMESITE = "Lax"
    
    # Development cache (in-memory)
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique-snowflake",
        }
    }

# ============================================================================
# SITE CONFIGURATION
# ============================================================================
SITE_ID = 1