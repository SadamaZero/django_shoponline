# Generated by Django 2.0.4 on 2018-04-26 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_auto_20180426_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodsinfo',
            name='pic',
            field=models.ImageField(upload_to='static/media/img'),
        ),
    ]
