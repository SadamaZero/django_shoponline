# Generated by Django 2.0.4 on 2018-04-26 05:33

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('pic', models.ImageField(upload_to='goods')),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('isDeltet', models.BooleanField(default=False)),
                ('unit', models.CharField(default='500g', max_length=20)),
                ('click', models.ImageField(upload_to='')),
                ('summary', models.CharField(max_length=200)),
                ('content', tinymce.models.HTMLField()),
                ('stock', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TypeInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('isDelete', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='goodsinfo',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.TypeInfo'),
        ),
    ]
