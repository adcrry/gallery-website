import csv
import io

import api.models as models
from api.models import Gallery
from django.contrib.auth import models as models2
from django.contrib.auth.decorators import user_passes_test
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .settings import BASE_DIR, LOGIN_REDIRECT_URL, LOGIN_URL


def root_redirect(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse(LOGIN_REDIRECT_URL))
    else:
        return HttpResponseRedirect(reverse(LOGIN_URL))


def media(request, path):
    """
    When trying to access /media/path this function makes sures the user is authenticated.
    If it is the case then the media is served by the nginx server.
    Otherwise an http access error code is sent back.
    """
    user = request.user
    dirs = path.split("/")
    gallery = Gallery.objects.filter(slug=dirs[0])
    if gallery.count() == 0:
        print("gallery not found")
        return HttpResponseForbidden()
    else:
        access_granted = gallery.first().can_user_access(user)

    if access_granted:
        response = HttpResponse()
        # Content-type will be detected by nginx
        del response["Content-Type"]
        response["X-Accel-Redirect"] = "/protected/media/" + path
        return response
    else:
        return HttpResponseForbidden()


def gallery(request, slug=""):
    context = {"slug": slug}
    return render(request, "gallery.html", context)


def galleries(request):
    return render(request, "galleries.html")


def expositions(request):
    return render(request, "expositions.html")


def index(request):
    return render(request, "index.html")


def material(request):
    return render(request, "material.html")


def videos(request):
    return render(request, "videos.html")


@user_passes_test(lambda u: u.is_superuser)
def add_promo(request):
    order = "nom, prénom, mail"
    context = {
        "order": order,
    }
    if request.method == "GET":
        return render(request, "add_promo.html", context)

    if "file" in request.FILES:
        csv_file = request.FILES["file"]
    else:
        context = {
            "order": order,
            "no_file": True,
            "promo_not_added": True,
        }
        return render(request, "add_promo.html", context)

    if not csv_file.name.endswith(".csv"):
        context = {
            "order": order,
            "type_error": True,
            "promo_not_added": True,
        }
        return render(request, "add_promo.html", context)
    data_set = csv_file.read().decode("UTF-8")
    io_string = io.StringIO(data_set)
    next(io_string)
    students_not_added = []
    for column in csv.reader(io_string, delimiter=";", quotechar="|"):
        password = models2.User.objects.make_random_password()
        debut = column[3].split("@")[0]
        if len(debut.split(".")[1].split("-")) > 1:
            username = debut.split(".")[0][0] + "." + debut.split(".")[1]
        else:
            username = debut.lower()
            print(username)
        user, created = models2.User.objects.get_or_create(
            last_name=column[1],
            first_name=column[2],
            username=username,
            email=column[3],
        )
        if created:
            user.set_password(password)
            user.save()
        if not created:
            students_not_added.append(
                (column[2] + "." + column[1]).replace(" ", "-").lower()
            )
    context = {
        "order": order,
        "promo_added": True,
        "students_not_added": students_not_added,
    }
    return render(request, "add_promo.html", context)
