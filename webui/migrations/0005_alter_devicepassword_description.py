# Generated by Django 5.1.3 on 2024-11-11 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webui', '0004_customuserdata_fullname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicepassword',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
