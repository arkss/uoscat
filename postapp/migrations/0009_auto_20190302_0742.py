# Generated by Django 2.1.7 on 2019-03-02 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postapp', '0008_auto_20190302_0741'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='voting',
        ),
        migrations.AddField(
            model_name='cat',
            name='voting',
            field=models.BooleanField(default=False),
        ),
    ]
