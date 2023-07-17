from django.urls import path
from api.views import (
    getRoutes,
    get_galleries,
    get_pics,
    create_gallery,
    create_promo,
    create_year,
    load_folder_into_gallery,
    delete_gallery,
    get_gallery,
    delete_pic,
    generate_thumbnails,
    import_users,
    FileUploadView,
)

urlpatterns = [
    path("", getRoutes),
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
]
