# Generated by Django 5.1.7 on 2025-03-31 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_accident_dispatched_police'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accident',
            name='dispatched_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
