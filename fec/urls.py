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
from apps.ec.views import prod_list, prod_detail, add_to_cart, get_cart_info, checkout

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^$', index, name='index'),
    url(r'^$', prod_list, name='index'),
    url(r'^accounts/login/$', login, {'template_name': 'fec/login.html'}, name='login'),
    url(r'^logout/$', logout_then_login, name='logout'),
    url(r'^register/$', register, name='register'),
    url(r'^test/', test, name='test'),
    # ec urls
    url(r'^prod_list/', prod_list, name='prod_list'),
    url(r'^prod_detail/(?P<prod_id>\d+)/$', prod_detail, name='prod_detail'),
    url(r'^add_to_cart/', add_to_cart, name='add_to_card'),
    url(r'^cart/', get_cart_info, name='get_cart_info'),
    url(r'^checkout/', checkout, name='checkout'),
]

urlpatterns += [
    url(r'^ec/', include('apps.ec.urls', namespace='ec')),
]
