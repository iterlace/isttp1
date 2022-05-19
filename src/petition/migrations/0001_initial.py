# Generated by Django 4.0.4 on 2022-05-19 18:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Petition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(db_index=True, max_length=200, verbose_name='Title')),
                ('description', models.TextField(max_length=2400, verbose_name='Description')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created')),
                ('votes_cache', models.PositiveIntegerField(blank=True, default=0, verbose_name='Votes')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
            ],
            options={
                'verbose_name': 'Petition',
                'verbose_name_plural': 'Petitions',
                'db_table': 'petition_petition',
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField(blank=True, default=None, max_length=400, null=True, verbose_name='Reason')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created')),
                ('petition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='petition.petition', verbose_name='Petition')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Vote',
                'verbose_name_plural': 'Votes',
                'db_table': 'petition_vote',
            },
        ),
        migrations.CreateModel(
            name='PetitionNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(db_index=True, max_length=40, verbose_name='Title')),
                ('description', models.TextField(max_length=300, verbose_name='Description')),
                ('path', models.TextField(blank=True, max_length=240, null=True, verbose_name='Reference path')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created')),
                ('petition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='petition.petition', verbose_name='Petition')),
            ],
            options={
                'verbose_name': 'Petition News',
                'verbose_name_plural': 'Petition News',
                'db_table': 'petition_notifications',
            },
        ),
        migrations.CreateModel(
            name='PetitionNews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(db_index=True, max_length=200, verbose_name='Title')),
                ('description', models.TextField(max_length=2400, verbose_name='Description')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created')),
                ('petition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='petition.petition', verbose_name='Petition')),
            ],
            options={
                'verbose_name': 'Petition News',
                'verbose_name_plural': 'Petition News',
                'db_table': 'petition_news',
            },
        ),
    ]
