# Generated by Django 5.1.3 on 2024-11-12 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webui', '0002_remove_userddata_groups_remove_userddata_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='port',
            field=models.IntegerField(default=22),
        ),
    ]
