from datetime import datetime

from django.contrib.auth import models as models2
from django.db import models


class Year(models.Model):
    year_id = models.IntegerField(default=0)
    name = models.CharField(primary_key=True, max_length=10)

    """
        Shitty way to add an auto increment field to a model without setting it to primary key
        Mandatory because I set the year_id as primary key and I can't change it to avoid breaking the database
    """

    def save(self, *args, **kwargs):
        if self._state.adding:
            last_id = Year.objects.all().aggregate(largest=models.Max("year_id"))[
                "largest"
            ]
            if last_id is not None:
                self.year_id = last_id + 1

        super(Year, self).save(*args, **kwargs)


class Promo(models.Model):
    name = models.CharField(primary_key=True, max_length=10)
    first_year = models.ForeignKey(Year, on_delete=models.PROTECT)


class Student(models.Model):
    user = models.OneToOneField(models2.User(), on_delete=models.PROTECT)
    promo = models.ForeignKey(Promo, on_delete=models.PROTECT)


class Gallery(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(blank=False, max_length=1000, unique=True)
    slug = models.SlugField(max_length=1000, blank=False, default="")
    description = models.CharField(max_length=10000)
    date = models.DateTimeField(blank=False, default=datetime.now)

    class Visibility(models.TextChoices):
        PUBLIC = "publique"
        SCHOOL = "école"
        PRIVATE = "privée"

    visibility = models.CharField(
        choices=Visibility.choices, default=Visibility.PRIVATE, max_length=10
    )

    class Type(models.TextChoices):
        PHOTO = "photo"
        VIDEO = "video"

    type = models.CharField(
        blank=False, default=Type.PHOTO, choices=Type.choices, max_length=10
    )
    year = models.ForeignKey(Year, on_delete=models.PROTECT, default=None)

    class View(models.TextChoices):
        GALLERY = "galerie"
        EXPOSITION = "exposition"

    view = models.CharField(
        blank=False, default=View.GALLERY, choices=View.choices, max_length=20
    )

    def can_user_access(self, user):
        if not user.is_authenticated and (
            not self.visibility == Gallery.Visibility.PUBLIC
        ):
            return False
        elif (
            not user.is_staff
            and not user.is_superuser
            and self.visibility is Gallery.Visibility.PRIVATE
        ):
            return False
        elif (
            not user.is_staff
            and not user.is_superuser
            and self.year.year_id < user.student.promo.first_year.year_id
        ):
            return False
        else:
            return True


class File(models.Model):
    id = models.AutoField(primary_key=True)
    file_name = models.CharField(blank=False, max_length=1000)
    file_extension = models.CharField(blank=False, max_length=100)
    file_full_name = models.CharField(blank=False, max_length=1100)
    link = models.CharField(max_length=10000)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, default=None)


class Video(models.Model):
    name = models.CharField(max_length=1000)
    slug = models.SlugField(max_length=1000, blank=False, default="")
    year = models.ForeignKey(Year, on_delete=models.PROTECT, default=None)
    date = models.DateTimeField(blank=False, default=datetime.now)
    video_url = models.URLField(max_length=2000)


class Reaction(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)


class Material(models.Model):
    name = models.CharField(max_length=1000)


class Face(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)


"""
class Teams(models.Model):
    year = models.IntegerChoices(default=Student.Promotion.P25 ,choices=Student.Promotion.choices)
    members = models.onTo

"""
