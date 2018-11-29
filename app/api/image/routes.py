from app.api.image.facade import ImageFacade
from app.models import Image


def register_image_api_urls(app):
    registrar = app.api_url_registrar

    registrar.register_get_routes(Image, ImageFacade)
    registrar.register_post_routes(Image, ImageFacade)
    registrar.register_patch_routes(Image, ImageFacade)
    registrar.register_delete_routes(Image, ImageFacade)

    registrar.register_relationship_get_route(ImageFacade, 'document')
    registrar.register_relationship_post_route(ImageFacade, 'document')
    registrar.register_relationship_patch_route(ImageFacade, 'document')
