# Generated by Django 2.2.3 on 2019-07-18 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('git_land', '0003_auto_20190717_0640'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='name',
            field=models.CharField(max_length=75, null=True),
        ),
        migrations.AlterField(
            model_name='ssh_key',
            name='ssh_key',
            field=models.TextField(),
        ),
    ]