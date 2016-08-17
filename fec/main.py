# -*- coding: utf8 -*-

from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from apps.ec.models import Cust
import logging


# Create your views here.


def index(request):
    return render(request,
                  'fec/index.html')


@login_required
def test(request):
    return render(request,
                  'fec/pseudo-element-before-after.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        form = UserCreationForm({'username': username,
                                 'password1': password1,
                                 'password2': password2})
        if form.is_valid():
            form.save()
            # 保存ec客户信息
            cust = Cust()
            cust.user_id = User.objects.get(username=username).id
            cust.name = username
            cust.created_date = timezone.now()
            cust.updated_date = timezone.now()
            cust.status = 1
            cust.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request,
                  'fec/register.html',
                  {'form': form, })


# 通过查看django login()源码, 实现在模板中fec/register.html指定input的next, 在form提交后redirect至next指向的地址
# def register(request,
#              template_name='fec/register.html',
#              redirect_field_name=REDIRECT_FIELD_NAME):
#     if request.method == 'POST':
#         # form = UserCreationForm(request.POST)
#         redirect_to = request.POST.get(redirect_field_name,
#                                        request.GET.get(redirect_field_name, ''))
#
#         print 'register_redirect_to1' + request.GET.get('redirect_field_name', '') + REDIRECT_FIELD_NAME
#         print 'register_redirect_to2' + redirect_to
#
#         username = request.POST.get('username', '')
#         password1 = request.POST.get('password1', '')
#         password2 = request.POST.get('password2', '')
#         form = UserCreationForm({'username': username, 'password1': password1, 'password2': password2})
#         if form.is_valid():
#             form.save()
#             return redirect(redirect_to)
#     else:
#         form = UserCreationForm()
#     return render(request, 'fec/register.html', {
#         'form': form,
#     })
