from django.contrib import admin

from . import models

admin.site.register(models.Report)
admin.site.register(models.Post)
admin.site.register(models.Source)
admin.site.register(models.PostImage)
admin.site.register(models.Favorite)
admin.site.register(models.Archive)
admin.site.register(models.Spam)
admin.site.register(models.Tag)
