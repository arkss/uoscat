# Generated by Django 2.1.7 on 2019-03-10 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('postapp', '0010_auto_20190310_2209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cat',
            name='habitat_x',
        ),
        migrations.RemoveField(
            model_name='cat',
            name='habitat_y',
        ),
    ]