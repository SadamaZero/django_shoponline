from django.db import models
from tinymce.models import HTMLField


class TypeInfo(models.Model):
    title = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class GoodsInfo(models.Model):
    name = models.CharField(max_length=20)
    pic = models.ImageField(upload_to='static/media/goods')
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)  # 最多位数，小数点后位数
    isDeltet = models.BooleanField(default=False)
    unit = models.CharField(max_length=20, default='500g')  # 单位
    click = models.IntegerField()
    summary = models.CharField(max_length=200)
    content = HTMLField()
    stock = models.IntegerField()
    type = models.ForeignKey(TypeInfo, on_delete=models.CASCADE)
