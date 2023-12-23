from api.models import Gallery
from django.contrib.auth.decorators import user_passes_test
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from galerie.loader import load_zip_into_gallery
from galerie.utils import get_random_string


@user_passes_test(lambda u: u.is_superuser)
def index_view(request):
    return render(request, "gestionindex.html")


@user_passes_test(lambda u: u.is_superuser)
def gallery_view(request, slug=""):
    context = {"slug": slug}
    if request.method == "POST" and request.FILES["zipfile"]:
        file = request.FILES["zipfile"]
        fs = FileSystemStorage()
        filename = fs.save(get_random_string(8) + ".zip", file)
        uploaded_file_url = fs.url(filename)

        gal = Gallery.objects.get(slug=slug)
        print(uploaded_file_url.split("/")[2])
        load_zip_into_gallery(uploaded_file_url.split("/")[2], gal)
        fs.delete(filename)
    return render(request, "gestiongallery.html", context)
