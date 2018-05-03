from django.shortcuts import render, redirect
from user_authentication import user_decorator
from django.db import transaction
from .models import OrderInfo, OrderDetail
from cart.models import Cart
from user_authentication.models import UserInfo
from datetime import datetime
from decimal import Decimal


@user_decorator.login_status
def create_order(request):
    user_id = request.session['user_id']
    user = UserInfo.objects.filter(id=user_id)
    context = {
        'user': user[0]
    }
    return render(request, 'order/submit_order.html', context)


'''
订单处理
1.创建订单
2.核对库存
3.创建详细清单
4.修改库存
5.删购物车
'''
@transaction.atomic  # 事务处理
@user_decorator.login_status
def order_handle(request):
    tran = transaction.savepoint()

    cart_ids = request.GET.get('cart_id')
    try:
        order_new = OrderInfo()
        now_time = datetime.now()
        uid = request.sessionp['user_id']
        order_new.oid = '%s%d' % (now_time.strftime('%Y%m%d%H%M%S'), uid)
        order_new.user_id = uid
        order_new.date = now_time
        order_new.total_to_pay = Decimal(request.GET.get('total2pay'))
        order_new.save()
        # 详细清单
        cart_list = [int(item) for item in cart_ids.split(',')]
        for detail_id in cart_list:
            detail =  OrderDetail()
            detail.order = order_new
            cart = Cart.objects.get(id=detail_id)

            # 库存操作
            goods = cart.goods
            if goods.stock >= cart.count:
                goods.stock = cart.goods.stock - cart.count
                goods.save()

                detail.goods_id = goods.id
                detail.unit_price = goods.unit_price
                detail.count = cart.count
                detail.save()

                # 清除购物车
                cart.delete()
            else:  # 库存不足,返回购物车修改
                transaction.savepoint_rollback(tran)  # 回退存档点
                return redirect('/user/cart/')

            transaction.savepoint_commit(tran)
    except Exception as e:
        print('----------%s-----------') % e
        transaction.savepoint_rollback(tran)

    return redirect('/user/center_order/')
