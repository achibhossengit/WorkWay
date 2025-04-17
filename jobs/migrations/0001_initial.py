# Generated by Django 5.2 on 2025-04-17 15:32

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('workplace', models.CharField(choices=[('H', 'Home'), ('O', 'Office'), ('Hy', 'Hybrid')], default='O', max_length=10)),
                ('status', models.CharField(choices=[('F', 'Full Time'), ('H', 'Half Time'), ('I', 'Intern')], default='F', max_length=10)),
                ('locations', models.CharField(max_length=250)),
                ('min_salary', models.PositiveIntegerField(verbose_name=django.core.validators.MinValueValidator(1000))),
                ('deadline', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('education', models.CharField(choices=[('J.S.C', 'J.S.C'), ('S.S.C', 'S.S.C'), ('H.S.C', 'H.S.C'), ('Master', 'Master')], max_length=10)),
                ('experience', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(30)])),
                ('skill', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('published_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.category')),
            ],
        ),
    ]
