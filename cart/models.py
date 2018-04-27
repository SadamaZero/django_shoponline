from django.db import models


# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey('user_authentication.UserInfo', on_delete=models.DO_NOTHING)  # 关联另一app的模型
    goods = models.ForeignKey('goods.GoodsInfo', on_delete=models.DO_NOTHING)
    count = models.IntegerField()
