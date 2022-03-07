# Generated by Django 4.0.3 on 2022-03-07 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Library_Browser', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.ManyToManyField(null=True, to='Library_Browser.author'),
        ),
    ]
