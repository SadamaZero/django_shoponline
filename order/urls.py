from django.urls import path
from . import views

# /user/submit_order/
urlpatterns = [
    path('', views.create_order, name='order_page'),
    path('order_handle', views.order_handle),
]
