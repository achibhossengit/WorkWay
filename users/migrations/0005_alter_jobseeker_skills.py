# Generated by Django 5.2 on 2025-07-01 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_jobseeker_about_jobseeker_experiences_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobseeker',
            name='skills',
            field=models.JSONField(default=list),
        ),
    ]
