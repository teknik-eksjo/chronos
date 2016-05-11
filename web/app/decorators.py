from .models import Permission
from flask import abort
from flask_login import current_user
from functools import wraps


def permission_required(permission):
    """Decorator which defines which permissions is required to access the given page."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    """Decorator for when admin permissions is required."""
    return permission_required(Permission.ADMINISTER)(f)
