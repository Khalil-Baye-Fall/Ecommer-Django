# Generated by Django 3.1.4 on 2020-12-09 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Business', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
