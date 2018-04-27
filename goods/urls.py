from django.urls import path
from . import views

# /
urlpatterns = [
    path('index/', views.index, name='main_page'),
    path('list<int:tid>_<int:pindex>_<int:sort>/', views.goods_list),
    path('detail_<int:g_id>/', views.good_detail),
]



