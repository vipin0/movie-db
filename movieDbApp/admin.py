from django.contrib import admin
from movieDbApp.models import Movie,StreamingPlatform,Review,Star
# Register your models here.
admin.site.register(Movie)

admin.site.register(StreamingPlatform)
admin.site.register(Review)
admin.site.register(Star)


