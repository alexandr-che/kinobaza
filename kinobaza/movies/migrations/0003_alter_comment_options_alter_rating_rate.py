# Generated by Django 5.0.4 on 2024-04-27 16:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_alter_starrating_options_movie_link_movie'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-id'], 'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментраии'},
        ),
        migrations.AlterField(
            model_name='rating',
            name='rate',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='movies.starrating'),
        ),
    ]
