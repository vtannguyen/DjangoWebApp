# Generated by Django 2.2 on 2019-06-06 03:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yelpCamp', '0004_auto_20190508_1446'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['timestamp']},
        ),
    ]