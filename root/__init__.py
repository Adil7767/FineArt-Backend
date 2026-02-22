# Optional: Celery may fail to import on some Python versions (e.g. 3.14). Runserver works without it.
try:
    from .celeryy import app as celery_app
except ImportError:
    celery_app = None

__all__ = ('celery_app',)
