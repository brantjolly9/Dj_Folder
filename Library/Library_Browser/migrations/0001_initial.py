# Generated by Django 4.0.3 on 2022-03-07 21:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default=None, max_length=200)),
                ('last_name', models.CharField(default=None, max_length=200)),
                ('middle_initial', models.CharField(default=None, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=None, max_length=200)),
                ('pageCount', models.IntegerField(default=0)),
                ('publishedDate', models.DateField(default=django.utils.timezone.now)),
                ('content', models.FileField(default='0', upload_to='')),
                ('synopsis', models.CharField(default='0', max_length=1000)),
                ('isbn', models.CharField(default='0', max_length=200)),
                ('msrp', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('imageLink', models.CharField(default='No Link', max_length=200)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Library_Browser.author')),
            ],
        ),
    ]
