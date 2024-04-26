from django.contrib import admin

from movies.models import *


admin.site.register(Comment)
admin.site.register(StarRating)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    fields = [
        ('title', 'slug', 'link_movie'),
        ('year', 'duration', 'quality', 'poster'),
        'description',
        ('actors', 'director', 'genre', 'country')
    ]
    prepopulated_fields = {'slug': ['title']}

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    fields = ['name', 'slug']
    prepopulated_fields = {'slug': ['name']}

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    fields = ['name', 'slug']
    prepopulated_fields = {'slug': ['name']}

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    fields = ['name', 'slug']
    prepopulated_fields = {'slug': ['name']}

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    fields = ['name', 'slug']
    prepopulated_fields = {'slug': ['name']}

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = [
        'movie', 'rate', 'user'
    ]
