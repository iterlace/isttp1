# Generated by Django 4.0.4 on 2022-05-19 21:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('petition', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='petitionnotification',
            name='petition',
        ),
        migrations.AddField(
            model_name='petitionnotification',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL, verbose_name='User'),
            preserve_default=False,
        ),
    ]
