
from flask_login import current_user
from functools import wraps

from app.api.decorators import error_403_privileges
from app.models import Document


def manage_publication_status():
    def wrap(view_function):
        @wraps(view_function)
        def wrapped_f(*args, **kwargs):

            if 'id' in kwargs:
                if current_user.is_anonymous:
                    doc = Document.query.filter(Document.id == kwargs['id']).first()
                    if doc and not doc.is_published:
                        return error_403_privileges

            return view_function(*args, **kwargs)

        return wrapped_f

    return wrap

