from django import template

from movies.models import Comment, Genre, Movie


register = template.Library()


@register.inclusion_tag('movies/inclusions_tags/about_movie.html')
def about_movie(movie):
    actors = [actor.name for actor in movie.actors.all()]
    genres = [genre.name for genre in movie.genre.all()]
    countries = [country.name for country in movie.country.all()]
    directors = [director.name for director in movie.director.all()]

    return {
        'movie': movie,
        'actors': actors,
        'genres': genres,
        'countries': countries,
        'directors': directors,
    }


@register.inclusion_tag('movies/inclusions_tags/comments.html')
def show_comments(movie):
    comments = movie.to_movie.filter(to_movie=movie.pk)
    return {'comments': comments}


@register.inclusion_tag('movies/inclusions_tags/categories.html')
def show_categories():
    genres = Genre.objects.all()
    return {'genres': genres}


@register.inclusion_tag('movies/inclusions_tags/years.html')
def show_years():
    years = [year.get('year') for year in Movie.objects.values('year')]
    return {'years': years}
