from api.models import Face, File, Gallery, Promo, Student, Video, Year
from django.contrib import admin


class YearAdmin(admin.ModelAdmin):
    list_display = ("name",)


class GalleryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "description",
        "date",
        "visibility",
        "type",
        "year",
        "view",
    )
    ordering = ("date",)


class FileAdmin(admin.ModelAdmin):
    list_display = ("gallery", "file_full_name", "file_name", "file_extension", "link")
    ordering = ("gallery",)


class PromoAdmin(admin.ModelAdmin):
    list_display = ("name", "first_year")


class StudentAdmin(admin.ModelAdmin):
    list_display = ("user", "promo")


class FaceAdmin(admin.ModelAdmin):
    list_display = ("student", "file")


class VideoAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "year", "date", "video_url")


# Register your models here.
admin.site.register(Year, YearAdmin)
admin.site.register(Promo, PromoAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Face, FaceAdmin)
admin.site.register(Video, VideoAdmin)
