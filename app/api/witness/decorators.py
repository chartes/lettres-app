
from functools import wraps


#TODO réussir à écrire un décorateur qui est exécuté APRES la fonction

def update_iiif_manifest_and_collections():
    def wrap(view_function):
        @wraps(view_function)
        def wrapped_f(*args, **kwargs):

            if 'id' in kwargs:
                pass

            return view_function(*args, **kwargs)

        return wrapped_f

    return wrap

