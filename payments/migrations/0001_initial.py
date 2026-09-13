from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('jobs', '0002_job_featured_until'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purpose', models.CharField(choices=[('featured', 'Featured Job Listing')], default='featured', max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(default='BDT', max_length=8)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('success', 'Success'), ('failed', 'Failed'), ('cancelled', 'Cancelled')], default='pending', max_length=12)),
                ('tran_id', models.CharField(max_length=40, unique=True)),
                ('val_id', models.CharField(blank=True, default='', max_length=80)),
                ('session_key', models.CharField(blank=True, default='', max_length=120)),
                ('gateway_url', models.URLField(blank=True, default='', max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='users.employer')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='jobs.job')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
