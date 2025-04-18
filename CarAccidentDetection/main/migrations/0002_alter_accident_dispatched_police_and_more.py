# Generated by Django 5.1.7 on 2025-03-30 08:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='accident',
            name='dispatched_police',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dispatched_accidents', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='accident',
            name='dispatched_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='accident',
            name='verified_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='accident',
            name='verifier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accidents', to=settings.AUTH_USER_MODEL),
        ),
    ]
