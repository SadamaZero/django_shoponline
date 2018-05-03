from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, reverse
from django.http import JsonResponse
from .models import UserInfo
from hashlib import sha1
from . import user_decorator
from goods.models import GoodsInfo



def register(request):
    context = {
        'title': '新用户注册',
    }
    return render(request, 'user_authentication/register.html', context)


def register_handle(request):
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd_repeat = post.get('cpwd')
    uemail = post.get('email')

    if upwd != upwd_repeat:
        return redirect('/user/register')

     # 密码加密
    s1 = sha1()
    s1.update(upwd.encode("utf8"))
    upwd_hash = s1.hexdigest()

    user = UserInfo()
    user.uname = uname
    user.upwd = upwd_hash
    user.uemail = uemail
    user.save()
    # 跳转到登陆页
    return redirect('/user/login/')


# 判断用户名是否已存在
def register_exist(request):
    uname_check = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname_check).count()
    return JsonResponse({'count': count})


def login(request):
    from_page = request.GET.get('from')
    uname = request.COOKIES.get('uname', '')
    context = {
        'title': '用户登陆',
        'error_name': 0,
        'error_pwd': 0,
        'uname': uname,
    }
    res = render(request, "user_authentication/login.html", context)
    res.set_cookie('url_from', from_page)
    return res


def login_handle(request):
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu', 0)

    user = UserInfo.objects.filter(uname=uname)  # 返回列表 get空时抛异常，需要try
    if user:
        # 存在此用户,加密比对
        s1 = sha1()
        s1.update(upwd.encode("utf8"))
        if s1.hexdigest() == user[0].upwd:
            # 密码验证通过,转到from
            url_from = request.COOKIES.get('url_from', '/index/')
            page = HttpResponseRedirect(url_from, reverse('main_page'))  # 直接redirect不能设cookies
# =======
#             page = HttpResponseRedirect(url_from)  # 直接redirect不能设cookies
# >>>>>>> da9dbe218ba95d52956563521e414580bcea717a

            # 是否保存用户名
            if jizhu != 0:
                page.set_cookie('uname', uname)
            else:
                page.set_cookie('uname', '', max_age=-1)  # 立即过期

            request.session['user_id'] = user[0].id
            request.session['user_name'] = uname
            return page

        else:
            context = {}
            context['title'] = '用户登陆'
            context['error_name'] = 0
            context['error_pwd'] = 1
            context['uname'] = uname
            context['upwd'] = upwd

            return render(request, 'user_authentication/login.html', context)
    else:
        context = {}
        context['title'] = '用户登陆'
        context['error_name'] = 1
        context['error_pwd'] = 0
        context['uname'] = uname
        context['upwd'] = upwd

        return render(request, 'user_authentication/login.html', context)


def logout_handle(request):
    request.session.flush()
    return redirect('/index/')


@user_decorator.login_status
def center_info(request):
    email = UserInfo.objects.get(id=request.session['user_id']).uemail

    # 查询最近浏览
    goods_recent_cookie = request.COOKIES.get('goods_recent_cookie', '4')
    goods_recent_l = goods_recent_cookie.split(',')
    goods_list = []
    for goods_id in goods_recent_l:
        goods_recent = GoodsInfo.objects.get(id=int(goods_id))
        goods_list.append(goods_recent)

    context = {
        'title': '用户中心',
        'user_email': email,
        'user_name': request.session['user_name'],
        'page_name': 1,
        'goods_list': goods_list
    }

    return render(request, 'user_authentication/user_center_info.html', context)
# =======
#     return render(request, 'user_authentication/user_center_info.html')
# >>>>>>> da9dbe218ba95d52956563521e414580bcea717a


@user_decorator.login_status
def center_order(request):
    return render(request, 'user_authentication/user_center_order.html')


@user_decorator.login_status
def center_site(request):
    return render(request, 'user_authentication/user_center_site.html')
