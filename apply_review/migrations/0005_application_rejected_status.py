from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apply_review', '0004_review_unique_together'),
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
                    ('X', 'Rejected'),
                    ('C', 'Cancelled'),
                ],
                default='P',
                max_length=1,
            ),
        ),
    ]
