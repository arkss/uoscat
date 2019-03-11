# Generated by Django 2.1.7 on 2019-03-10 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('postapp', '0009_auto_20190302_0742'),
    ]

    operations = [
        migrations.CreateModel(
            name='habitat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
            ],
        ),
        migrations.AlterField(
            model_name='cat',
            name='habitat_x',
            field=models.FloatField(default=37.5839),
        ),
        migrations.AlterField(
            model_name='cat',
            name='habitat_y',
            field=models.FloatField(default=127.0588),
        ),
        migrations.AddField(
            model_name='habitat',
            name='cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='postapp.Cat'),
        ),
    ]