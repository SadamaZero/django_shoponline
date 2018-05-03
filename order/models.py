from django.db import models


class OrderInfo(models.Model):
    oid = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey('user_authentication.UserInfo', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    is_pay = models.BooleanField(default=False)
    total_to_pay = models.DecimalField(max_digits=8, decimal_places=2)
    user_addr = models.CharField(max_length=200)


class OrderDetail(models.Model):
    goods = models.ForeignKey('goods.GoodsInfo', on_delete=models.DO_NOTHING)
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    count = models.IntegerField()
