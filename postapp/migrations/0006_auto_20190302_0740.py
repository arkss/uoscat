# Generated by Django 2.1.7 on 2019-03-02 07:40

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('postapp', '0005_auto_20190302_0739'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='created_at',
        ),
        migrations.AddField(
            model_name='vote',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 3, 2, 7, 40, 38, 15945, tzinfo=utc)),
        ),
    ]