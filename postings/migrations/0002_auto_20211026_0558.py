# Generated by Django 2.2.4 on 2021-10-26 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posting',
            name='content',
            field=models.CharField(max_length=1000),
        ),
    ]
