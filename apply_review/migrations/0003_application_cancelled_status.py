from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apply_review', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(
                choices=[
                    ('P', 'Pending'),
                    ('R', 'Reviewed'),
                    ('A', 'ACCEPT'),
                    ('C', 'Cancelled'),
                ],
                default='P',
                max_length=1,
            ),
        ),
    ]
