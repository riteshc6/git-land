# Generated by Django 2.2.3 on 2019-07-20 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('git_land', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='test_info',
            name='new_message',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
