# Generated by Django 3.1.3 on 2021-04-17 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='time_created',
            field=models.DateField(auto_now_add=True),
        ),
    ]
