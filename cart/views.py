from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from user_authentication import user_decorator
from .models import *


@user_decorator.login_status
def cart(request):
    user_id = request.session['user_id']
    cart_record = Cart.objects.filter(user_id=user_id)

    context = {
        'title': '购物车',
        'page_name': 1,
        'cart_record': cart_record,
    }
    return render(request, 'cart/cart.html', context)


@user_decorator.login_status
def add_to_cart(request, goods_id, count):
    user_id = request.session['user_id']
    # 查询购物车里是否有此用户的此商品的添加记录
    cart_record = Cart.objects.filter(user_id=user_id, goods_id=goods_id)
    if len(cart_record) >= 1:  # 修改
        cart_to_add = cart_record[0]
        cart_to_add.count = cart_to_add.count + count
        cart_to_add.save()
    else:  # 新建
        cart_to_add = Cart()
        cart_to_add.user_id = user_id
        cart_to_add.goods_id = goods_id
        cart_to_add.count = count
        cart_to_add.save()

    if request.is_ajax():
        count = Cart.objects.filter(user_id=request.session['user_id']).count()  # 车里有几种商品
        return JsonResponse({'count': count})
    else:
        return redirect(reverse('cart_index'))


def edit(request):
    pass


def delete(request):
    pass
