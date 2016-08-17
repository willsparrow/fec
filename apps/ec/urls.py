from django.conf.urls import include, url
from .views import *

# app_name = 'ec'

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^prod_list/', prod_list, name='prod_list'),
    url(r'^prod_detail/(?P<prod_id>\d+)/$', prod_detail, name='prod_detail'),
    url(r'^add_to_cart/', add_to_cart, name='add_to_card'),
    url(r'^add_prod/', add_prod, name='add_prod'),
    url(r'^del_prod/', del_prod, name='del_prod'),
    url(r'^cart/', get_cart_info, name='get_cart_info'),
    url(r'^checkout/$', checkout, name='checkout'),
]
