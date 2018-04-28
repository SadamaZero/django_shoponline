from django.http import HttpResponseRedirect


def login_status(func):
    def wrapper(request, *args, **kwargs):
        if 'user_id' in request.session:
            return func(request, *args, **kwargs)
        else:
            # redirect = HttpResponseRedirect('/user/login/')
            redirect = HttpResponseRedirect('/user/login/?from=/user/center_info/')
            # redirect.set_cookie('url_from', request.get_full_path())
# =======
#             redirect = HttpResponseRedirect('/user/login/')
#             redirect.set_cookie('url_from', request.get_full_path())
# >>>>>>> da9dbe218ba95d52956563521e414580bcea717a
            return redirect
    return wrapper
