from django.shortcuts import render, redirect
from django.http import JsonResponse
from user_authentication import user_decorator
from django.db import transaction
from .models import OrderInfo, OrderDetail
from cart.models import Cart
from user_authentication.models import UserInfo
from goods.models import GoodsInfo
from datetime import datetime
from decimal import Decimal


@user_decorator.login_status
def create_order(request):
    """
    此函数用户给下订单页面展示数据
    接收购物车页面GET方法发过来的购物车中物品的id，构造购物车对象供订单使用
    """
    user_id = request.session['user_id']
    user = UserInfo.objects.filter(id=user_id)

    # 获取勾选的每一个订单对象，构造成list，作为上下文传入下单页面
    cart_ids = request.GET.getlist('cart_id')
    item_in_order = []
    for item_id in cart_ids:
        item_in_order.append(Cart.objects.get(id=int(item_id)))

    context = {
        'title': '提交订单',
        'user': user[0],
        'goods_in_order_list': item_in_order,
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

    # cart_ids = request.GET.get('cart_id')
    try:
        post = request.POST
        cart_ids = post.getlist('id[]')
        total = post.get('total')
        address = post.get('address')
        # ------------------
        now_time = datetime.now()
        uid = request.session['user_id']

        order_new = OrderInfo()
        order_new.oid = '%s%d' % (now_time.strftime('%Y%m%d%H%M%S'), uid)
        order_new.user_id = uid
        order_new.date = now_time
        order_new.total_to_pay = total
        order_new.user_addr = address
        order_new.save()
        # 详细清单
        # cart_list = [int(item) for item in cart_ids.split(',')]
        for detail_id in cart_ids:
            # detail = OrderDetail()
            # detail.order = order_new
            cart = Cart.objects.get(id=detail_id)

            # 库存操作
            goods = GoodsInfo.objects.get(pk=cart.goods_id)
            if int(goods.stock) >= int(cart.count):
                goods.stock -= int(cart.count)
                goods.save()

                goods_in_order = GoodsInfo.objects.get(cart__id=detail_id)
                # 创建订单详情表
                detailinfo = OrderDetail()
                detailinfo.goods_id = int(goods_in_order.id)
                detailinfo.order_id = int(order_new.oid)
                detailinfo.unit_price = Decimal(int(goods_in_order.unit_price))
                detailinfo.count = int(cart.count)
                detailinfo.save()
                # detail.goods_id = goods.id
                # detail.unit_price = goods.unit_price
                # detail.count = cart.count
                # detail.save()

                # 清除购物车
                cart.delete()
            else:  # 库存不足,返回购物车修改
                transaction.savepoint_rollback(tran)  # 回退存档点
                return JsonResponse({'status': 2})

            transaction.savepoint_commit(tran)
    except Exception as e:
        print('----------%s-----------') % e
        transaction.savepoint_rollback(tran)

    return JsonResponse({'status': 1})
