# Generated by Django 2.2.1 on 2019-05-22 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0003_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.FileField(upload_to='document/'),
        ),
    ]
