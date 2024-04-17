from django.db import models
from django.contrib.auth.models import AbstractUser


def user_avatar_path(instance, filename):
    # instance - это экземпляр модели User
    # создаем путь сохранения файла в виде "users_username/avatars/{filename}"
    return f'user_{instance.username}/avatars/{filename}'


class User(AbstractUser):
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True,
                               null=True, verbose_name='Аватар')

    def __str__(self):
        return self.username
