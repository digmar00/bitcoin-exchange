# Generated by Django 3.0.5 on 2021-05-10 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20210508_1923'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='type',
            field=models.CharField(choices=[('1', 'Buy'), ('2', 'Sell')], default='1', max_length=4),
        ),
    ]
