from django.urls import path
from . import views

# /user/
urlpatterns = [
    path('register/', views.register, name='register'),
    path('register_handle/', views.register_handle),
    path('register_exist/', views.register_exist),
    path('login/', views.login, name='login'),
    path('login_handle/', views.login_handle),
    path('info/', views.info),
]
