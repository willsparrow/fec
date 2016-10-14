# -*- coding: utf8 -*-


import logging
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import *
from .forms import *
from django.db.models import Sum
from django.db.models import Count
from django.db.models import F

# Create your views here.

logger = logging.getLogger('django')

def index(request):
    return render(request, 'ec/index.html')


# 查询所有商品信息
def prod_list(request):
    prods = Prod.objects.all()
    logger.debug('查询所有商品信息')
    logger.debug(prods)
    add_to_cart_form = AddToCartForm(initial={'qty': 1})
    context_dict = {'prods': prods,
                    'add_to_cart_form': add_to_cart_form}
    return render(request,
                  'ec/prod_list.html',
                  context_dict)


# 查询某个商品的详情信息
def prod_detail(request, prod_id):
    prod = Prod.objects.get(id=prod_id)
    add_to_cart_form = AddToCartForm(initial={'qty': 1})
    context_dict = {'prod': prod,
                    'add_to_cart_form': add_to_cart_form}
    return render(request,
                  'ec/prod_detail.html',
                  context_dict)


# 创建订单
def create_order(cust_id):
    logger.debug('查询该客户是否有未处理的订单')
    cnt = So.objects.filter(cust_id=cust_id, status=1).annotate(cnt=Count('id'))
    logger.debug(cnt)
    if len(cnt) == 0:
        logger.debug('该客户还没有订单, 创建订单')
        so = So()
        cust = Cust.objects.get(id=cust_id)
        so.cust_id = cust.id
        so.cust_name = cust.name
        so.cust_mobilephone = cust.mobilephone
        so.cust_telephone = cust.telephone
        so.cust_email = cust.email
        so.shop = cust.shop
        so.company = cust.company
        so.province = cust.province
        so.city = cust.city
        so.address = cust.address
        so.created_date = timezone.now()
        so.updated_date = timezone.now()
        so.status = 1
        so.save()
        logger.debug('订单:' + str(so.id) + '已创建')
    else:
        so = So.objects.filter(cust_id=cust_id, status=1)[0]
        logger.debug('该客户有还未处理的订单:#' + str(so.id))
    return so.id


@login_required
def add_to_cart(request):
    cust_id = Cust.objects.get(user_id=User.objects.get(username=request.user.username).id).id
    # 创建订单
    so_id = create_order(cust_id)
    prod = Prod.objects.get(id=request.POST.get('prod_id'))
    # 创建订单行
    sol = Sol()
    sol.so_id = so_id
    sol.cust_id = cust_id
    sol.prod_id = prod.id
    sol.name = prod.name
    sol.img_t = prod.img_t
    sol.price = prod.price
    sol.qty = request.POST.get('qty')
    sol.created_date = timezone.now()
    sol.updated_date = timezone.now()
    sol.status = 1
    sol.save()
    logger.debug('创建订单行:#' + str(sol.id))
    qty = sol.qty
    amount = int(sol.qty) * prod.price
    context_dict = {'prod': prod,
                    'qty': qty,
                    'amount': amount}
    return render(request,
                  'ec/_add_to_cart_message.html',
                  context_dict)


def get_cart_detail(cust_id):
    # 查询该用户是否有购物车信息
    cnt = So.objects.filter(cust_id=cust_id, status=1).annotate(cnt=Count('id'))
    if len(cnt) == 0:
        context_dict = {'cnt': 0}
    else:
        # 对明细进行购物车展示聚合
        sols = Sol.objects.filter(cust_id=cust_id,
                                  status=1).values('so_id',
                                                   'prod_id',
                                                   'name',
                                                   'img_t',
                                                   'price').annotate(qty=Sum('qty'),
                                                                     amt=Sum('qty') * F('price'))
        # 聚合购物车商品总额
        total = Sol.objects.filter(cust_id=cust_id,
                                   status=1).values('so_id').annotate(total=Sum(F('qty') * F('price')))[0]['total']

        logger.debug('查询用户购物车信息')
        context_dict = {'sols': sols,
                        'total': total}

    return context_dict


@login_required
def get_cart_info(request):
    cust_id = Cust.objects.get(user_id=User.objects.get(username=request.user.username).id).id
    context_dict = get_cart_detail(cust_id)
    return render(request,
                  'ec/cart.html',
                  context_dict)


@login_required
def add_prod(request):
    cust_id = Cust.objects.get(user_id=User.objects.get(username=request.user.username).id).id
    so_id = create_order(cust_id)
    prod = Prod.objects.get(id=request.POST.get('prod_id'))
    # 创建订单行
    sol = Sol()
    sol.so_id = so_id
    sol.cust_id = cust_id
    sol.prod_id = prod.id
    sol.name = prod.name
    sol.img_t = prod.img_t
    sol.price = prod.price
    sol.qty = 1
    sol.created_date = timezone.now()
    sol.updated_date = timezone.now()
    sol.status = 1
    sol.save()
    logger.debug('创建订单行:#' + str(sol.id))
    qty = sol.qty
    amount = int(sol.qty) * prod.price
    context_dict = get_cart_detail(cust_id)
    return render(request,
                  'ec/_cart_detail.html',
                  context_dict)


@login_required
def del_prod(request):
    cust_id = Cust.objects.get(user_id=User.objects.get(username=request.user.username).id).id
    so_id = create_order(cust_id)
    prod = Prod.objects.get(id=request.POST.get('prod_id'))
    sol = Sol()
    sol.so_id = so_id
    sol.cust_id = cust_id
    sol.prod_id = prod.id
    sol.name = prod.name
    sol.img_t = prod.img_t
    sol.price = prod.price
    sol.qty = -1
    sol.created_date = timezone.now()
    sol.updated_date = timezone.now()
    sol.status = 1
    sol.save()
    logger.debug('创建订单行:#' + str(sol.id))
    qty = sol.qty
    amount = int(sol.qty) * prod.price
    context_dict = get_cart_detail(cust_id)
    return render(request,
                  'ec/_cart_detail.html',
                  context_dict)


@login_required
def checkout(request):
    cust = Cust.objects.get(user_id=User.objects.get(username=request.user.username).id)
    context_dict = {
        'cust': cust
    }
    return render(request,
                  'ec/checkout.html',
                  context_dict)


@login_required
def checkout_confirm(request):
    # 查询客户信息并修改客户的默认地址
    cust = Cust.objects.get(user_id=User.objects.get(username=request.user.username).id)
    cust.province = request.POST.get('province')
    cust.city = request.POST.get('city')
    cust.country = request.POST.get('area')
    cust.address = request.POST.get('detailAddress')
    cust.save()
    print request.POST.get('province')
    print request.POST.get('city')
    print request.POST.get('area')
    print request.POST.get('detailAddress')
    # 查询客户订单信息并修改修改订单的状态
    so = So.objects.filter(cust_id=cust.id, status=1)[0]
    so.status = 888
    so.save()
    # 查询客户订单对应的订单行信息并修改修改订单行的状态
    sols = Sol.objects.filter(cust_id=cust.id,
                              so_id=so.id,
                              status=1)
    for sol in sols:
        sol.status = 888
        sol.save()

    context_dict = {
        'cust': cust
    }
    return render(request,
                  'ec/checkout_confirm.html',
                  context_dict)
