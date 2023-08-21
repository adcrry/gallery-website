from api.views import (
    FileUploadView,
    change_visibility,
    create_gallery,
    create_promo,
    create_year,
    delete_gallery,
    delete_pic,
    generate_thumbnails,
    get_galleries,
    get_gallery,
    get_pics,
    getRoutes,
    import_users,
    load_folder_into_gallery,
    years,
    get_associated_pictures
)
from django.urls import path

urlpatterns = [
    path("", getRoutes, name="api-routes"),
    path("galleries/", get_galleries),
    path("gallery/load", load_folder_into_gallery),
    path("gallery/gen_thumb", generate_thumbnails),
    path("gallery/pics/", get_pics),
    path("gallery/pics/delete/", delete_pic),
    path("gallery/", get_gallery),
    path("gallery/delete/", delete_gallery),
    path("gallery/upload/", FileUploadView.as_view()),
    path("galleries/create/", create_gallery),
    path("promo/create/", create_promo),
    path("year/create/", create_year),
    path("import/", import_users),
    path("gallery/change_visibility/", change_visibility),
    path("years/", years),
    path("associated_pics/", get_associated_pictures),
]
