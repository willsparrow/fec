from django.conf.urls import include, url
from .views import *

# app_name = 'ec'

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^prod_list/$', get_prod_list, name='prod_list'),
    url(r'^prod_list/(?P<category>\w+)/$', get_prod_list_by_category, name='prod_list_by_category'),
    url(r'^search/', get_prod_list_by_keywords, name='prod_list_by_keywords'),
    url(r'^prod_detail/(?P<prod_id>\d+)/$', get_prod_detail, name='prod_detail'),
    url(r'^prod_pvs_json/(?P<prod_id>\d+)/$', get_prod_pvs_json, name='prod_pvs_json'),
    url(r'^prod_skus_json/(?P<prod_id>\d+)/$', get_prod_skus_json, name='prod_skus_json'),
    url(r'^add_to_cart/$', add_to_cart, name='add_to_card'),
    url(r'^add_sku_to_cart/$', add_sku_to_cart, name='add_sku_to_card'),
    url(r'^add_prod/$', add_prod, name='add_prod'),
    url(r'^del_prod/$', del_prod, name='del_prod'),
    url(r'^rmv_prod/$', rmv_prod, name='rmv_prod'),
    url(r'^add_sku/$', add_sku, name='add_sku'),
    url(r'^del_sku/$', del_sku, name='del_sku'),
    url(r'^rmv_sku/$', rmv_sku, name='rmv_sku'),
    url(r'^cart/$', get_cart_detail, name='get_cart_detail'),
    url(r'^checkout/$', checkout, name='checkout'),
    url(r'^checkout_confirm/$', checkout_confirm, name='checkout_confirm'),
    url(r'^order_list/$', get_order_list, name='order_list'),
    url(r'^order_detail/(?P<so_id>\d+)/$', get_order_detail, name='order_detail'),
    url(r'^wxpay/$', wxpay, name='wxpay'),
    url(r'^generate_wxpay_qrcode/(?P<order_id>\d+)/$', generate_wxpay_qrcode, name='generate_wxpay_qrcode'),
    url(r'^wxpay_callback/$', wxpay_callback, name='wxpay_callback'),
    url(r'^xml/$', xml, name='xml'),
    url(r'^xml_post/$', xml_post, name='xml_post'),
]
