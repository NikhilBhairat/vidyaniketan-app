from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_delete_questionpaper'),
    ]

    operations = [
        # Fix the read_at field to allow NULL values
        migrations.AlterField(
            model_name='notificationread',
            name='read_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        # Add created_at field to track when the record was created
        migrations.AddField(
            model_name='notificationread',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
