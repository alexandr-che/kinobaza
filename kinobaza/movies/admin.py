from django.contrib import admin

from movies.models import *


admin.site.register(Movie)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(Country)
admin.site.register(Genre)
admin.site.register(Director)
admin.site.register(Actor)
