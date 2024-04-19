from django import template

from movies.models import Comment, Genre, Movie


register = template.Library()


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
