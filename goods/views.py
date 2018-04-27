from django.shortcuts import render, HttpResponse
from django.core.paginator import Paginator, Page
from .models import *


def index(request):
    # 查询侧边栏各分类最新4条、最热4条数据
    typelist = TypeInfo.objects.all()
    type0_new = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type0_hot = typelist[0].goodsinfo_set.order_by('-click')[0:4]
    type1_new = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    type1_hot = typelist[1].goodsinfo_set.order_by('-click')[0:4]
    type2_new = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    type2_hot = typelist[2].goodsinfo_set.order_by('-click')[0:4]
    type3_new = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    type3_hot = typelist[3].goodsinfo_set.order_by('-click')[0:4]
    type4_new = typelist[4].goodsinfo_set.order_by('-id')[0:4]
    type4_hot = typelist[4].goodsinfo_set.order_by('-click')[0:4]
    type5_new = typelist[5].goodsinfo_set.order_by('-id')[0:4]
    type5_hot = typelist[5].goodsinfo_set.order_by('-click')[0:4]

    context = {}
    context['title'] = '生鲜|首页'
    context['type0_new'] = type0_new
    context['type0_hot'] = type0_hot
    context['type1_new'] = type1_new
    context['type1_hot'] = type1_hot
    context['type2_new'] = type2_new
    context['type2_hot'] = type2_hot
    context['type3_new'] = type3_new
    context['type3_hot'] = type3_hot
    context['type4_new'] = type4_new
    context['type4_hot'] = type4_hot
    context['type5_new'] = type5_new
    context['type5_hot'] = type5_hot
    return render(request, 'goods/index.html', context)


def goods_list(request, tid, pindex=1, sort=1):  # type_id,page_num,排序依据
    typeinfo = TypeInfo.objects.get(pk=tid)
    new_goods = typeinfo.goodsinfo_set.order_by('-id')[0:2]  # 侧边栏新品

    if sort == '1':  # 按上架时间
        # list_goods = new_goods
        list_goods = GoodsInfo.objects.filter(type_id=tid).order_by('-id')
    elif sort == '2':  # 价格排序
        list_goods = GoodsInfo.objects.filter(type_id=tid).order_by('-unit_price')
    else:  # 点击量
        list_goods = GoodsInfo.objects.filter(type_id=tid).order_by('-click')

    paginator = Paginator(list_goods, 10)
    page = paginator.get_page(pindex)

    context = {
        'title': '分类|'+typeinfo.title,
        'page': page,
        'paginator': paginator,
        'typeinfo': typeinfo,
        'sort': sort,
        'new_goods': new_goods
    }

    return render(request, 'goods/list.html', context)


def good_detail(request, g_id):
    good = GoodsInfo.objects.get(pk=g_id)
    good.click = good.click + 1
    good.save()
    new_goods = good.type.goodsinfo_set.order_by('-id')[0:2]
    context = {
        'title': '商品名|' + good.name,
        'good': good,
        'new_goods': new_goods,
        'id': g_id,
    }

    return render(request, 'goods/detail.html', context)
