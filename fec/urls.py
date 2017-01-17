"""fec URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout_then_login
from .main import *
from apps.ec.views import get_prod_list, get_prod_list_by_category, get_prod_list_by_keywords, get_prod_detail, add_to_cart, get_cart_detail, checkout, checkout_confirm, get_order_list, get_order_detail

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^$', index, name='index'),
    url(r'^$', get_prod_list, name='index'),
    url(r'^accounts/login/$', login, {'template_name': 'fec/login.html'}, name='login'),
    url(r'^logout/$', logout_then_login, name='logout'),
    url(r'^register/$', register, name='register'),
    url(r'^test/', test, name='test'),
    # ec urls
    url(r'^prod_list/$', get_prod_list, name='prod_list'),
    url(r'^prod_list/(?P<category>\w+)/$', get_prod_list_by_category, name='prod_list_by_category'),
    url(r'^search/$', get_prod_list_by_keywords, name='prod_list_by_keywords'),
    url(r'^prod_detail/(?P<prod_id>\d+)/$', get_prod_detail, name='prod_detail'),
    url(r'^add_to_cart/$', add_to_cart, name='add_to_card'),
    url(r'^cart/$', get_cart_detail, name='get_cart_detail'),
    url(r'^checkout/$', checkout, name='checkout'),
    url(r'^checkout_confirm/$', checkout_confirm, name='checkout_confirm'),
    url(r'^order_list/$', get_order_list, name='order_list'),
    url(r'^order_detail/(?P<so_id>\d+)/$', get_order_detail, name='order_detail'),
]

urlpatterns += [
    url(r'^ec/', include('apps.ec.urls', namespace='ec')),
]
