from django.urls import path
from . import views

# /user/cart/
urlpatterns = [
    path('', views.cart, name='cart_index'),
    path('add<int:goods_id>_<int:count>/', views.add_to_cart),
    path('edit_<int:cart_id>_<int:count>/', views.edit),
    path('delete_<int:cart_id>/', views.delete),
]
