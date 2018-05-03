from django.urls import path
from . import views

# /user/
urlpatterns = [
    path('register/', views.register, name='register'),
    path('register_handle/', views.register_handle),
    path('register_exist/', views.register_exist),
    path('login/', views.login, name='login'),
    path('login_handle/', views.login_handle),
    path('logout_handle/', views.logout_handle, name='logout'),
    path('center_info/', views.center_info, name='user_center'),
    path('center_order/', views.center_order, name='center_order'),
    path('center_site/', views.center_site, name='center_site'),
]
