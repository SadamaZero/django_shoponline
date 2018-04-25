from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from .models import UserInfo
from hashlib import sha1


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
    uname = request.COOKIES.get('uname', '')
    context = {
        'title': '用户登陆',
        'error_name': 0,
        'error_pwd': 0,
        'uname': uname,
    }

    return render(request, 'user_authentication/login.html', context)


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
            # 密码验证通过,转到主页
            page = HttpResponseRedirect('/user/info/')  # 直接redirect不能设cookies

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


def info(request):
    return render(request, 'user_authentication/user_center_info.html')
