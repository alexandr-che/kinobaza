from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from datetime import datetime

from users.models import User


year_now = datetime.now().year


def poster_movie_path(instance, filename):
    # instance - это экземпляр модели Movie
    # создаем путь сохранения файла в виде "posters/movie_<movie_name>/{filename}"
    return f'posters/movie_{instance.title}/{filename}'


class Movie(models.Model):

    QUALITY_CHOICES = [('HD', '720'), ('FULL-HD', '1080'), ('4K', '2160')]

    link_movie = models.CharField(max_length=255, verbose_name='Ссылка на фильм')
    slug = models.SlugField(max_length=255, unique=True)
    poster = models.ImageField(upload_to=poster_movie_path, blank=True, null=True)
    title = models.CharField(max_length=100, verbose_name='Название фильма')
    description = models.TextField('Описание')
    year = models.PositiveIntegerField(validators=[
        MinValueValidator(1895), MaxValueValidator(year_now)],
        verbose_name='Год выхода')
    duration = models.PositiveIntegerField(validators=[MaxValueValidator(1800)],
                                           verbose_name='Длительность (мин)')
    country = models.ManyToManyField('Country', verbose_name='Страна')
    genre = models.ManyToManyField('Genre', verbose_name='Жанры')
    quality = models.CharField(max_length=255, choices=QUALITY_CHOICES,
                               verbose_name='Качество')
    director = models.ManyToManyField('Director', verbose_name='Режиссер')
    actors = models.ManyToManyField('Actor', verbose_name='Актёры')

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural ='Фильмы'

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    comment = models.TextField(max_length=1000, blank=True, null=True, verbose_name='Текст комментария')
    to_movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='to_movie', verbose_name='Фильм')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    created_by = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-id']

    def __str__(self):
        return f'Комментарий к фильму {self.to_movie.title}'
    

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.ForeignKey('StarRating', on_delete=models.CASCADE, default=0)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie')

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

    def __str__(self):
        return f'Рейтинг к фильму {self.movie.title}'
    

class StarRating(models.Model):
    star = models.SmallIntegerField()

    class Meta:
        ordering = ['-star']

    def __str__(self):
        return f'{self.star}'


class Country(models.Model):
    name = models.CharField(max_length=100, verbose_name='Страна')
    slug = models.SlugField(max_length=100, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название жанра')
    slug = models.SlugField(max_length=100, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя режиссёра')
    slug = models.SlugField(max_length=100, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Режиссёр'
        verbose_name_plural = 'Режиссёры'

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя актёра')
    slug = models.SlugField(max_length=100, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Актёр'
        verbose_name_plural = 'Актёры'

    def __str__(self):
        return self.name
    

class Collections(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    movies = models.ManyToManyField(Movie, verbose_name='Фильмы')

    class Meta:
        verbose_name = 'Подборка'
        verbose_name_plural = 'Подборки'

    def __str__(self):
        return self.name


class FavoriteMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fav_user')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='fav_movie')

    def __str__(self):
        return f'User: {self.user.username}, Movie: {self.movie.title}'
