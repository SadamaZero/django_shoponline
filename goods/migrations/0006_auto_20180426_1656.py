# Generated by Django 2.0.4 on 2018-04-26 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0005_auto_20180426_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodsinfo',
            name='pic',
            field=models.ImageField(upload_to='goods'),
        ),
    ]
