from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apply_review', '0003_application_cancelled_status'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('employer', 'jobseeker')},
        ),
    ]
