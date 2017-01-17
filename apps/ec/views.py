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
def get_prod_list(request):
    prods = Prod.objects.all()
    logger.debug('查询所有商品信息')
    logger.debug(prods)
    add_to_cart_form = AddToCartForm(initial={'qty': 1})
    context_dict = {'prods': prods,
                    'add_to_cart_form': add_to_cart_form}
    return render(request,
                  'ec/prod_list.html',
                  context_dict)


# 根据商品类型查询该类型所有商品信息
def get_prod_list_by_category(request, category):
    cnt = Prod.objects.filter(category=category).count()
    if cnt == 0:
        context_dict = {'cnt': 0}
    else:
        prods = Prod.objects.filter(category=category)
        logger.debug('根据商品类型' + str(category) + '查询该类型所有商品信息')
        logger.debug(prods)
        add_to_cart_form = AddToCartForm(initial={'qty': 1})
        context_dict = {'prods': prods,
                        'add_to_cart_form': add_to_cart_form}
    return render(request,
                  'ec/prod_list.html',
                  context_dict)


# 查询某个商品的详情信息
def get_prod_detail(request, prod_id):
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
        so.country = cust.country
        so.address = cust.address
        so.amount = 0
        so.total = 0
        so.created_date = timezone.now()
        so.updated_date = timezone.now()
        so.status = 1
        so.save()
        logger.debug('订单#' + str(so.id) + '已创建')
    else:
        so = So.objects.filter(cust_id=cust_id, status=1)[0]
        logger.debug('该客户有还未处理的订单#' + str(so.id))
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
    logger.debug('创建订单行#' + str(sol.id))
    qty = sol.qty
    amount = int(sol.qty) * prod.price
    context_dict = {'prod': prod,
                    'qty': qty,
                    'amount': amount}
    return render(request,
                  'ec/_add_to_cart_message.html',
                  context_dict)


def get_cart_info(cust_id):
    # 查询该用户是否有购物车信息
    cust = Cust.objects.get(id=cust_id)
    cnt = So.objects.filter(cust_id=cust_id, status=1).annotate(cnt=Count('id'))
    if len(cnt) == 0:
        context_dict = {'cnt': 0,
                        'cust': cust}
    else:
        # 对明细进行购物车展示聚合
        sols = Sol.objects.filter(cust_id=cust_id,
                                  status=1).values('so_id',
                                                   'prod_id',
                                                   'name',
                                                   'img_t',
                                                   'price').annotate(qty=Sum('qty'),
                                                                     amt=Sum('qty') * F('price'))
        # 聚合购物车商品总数
        total = Sol.objects.filter(cust_id=cust_id,
                                   status=1).values('so_id').annotate(total=Sum(F('qty')))[0]['total']
        # 聚合购物车商品总额
        amount = Sol.objects.filter(cust_id=cust_id,
                                    status=1).values('so_id').annotate(amount=Sum(F('qty') * F('price')))[0]['amount']

        logger.debug('查询用户购物车信息')
        context_dict = {'sols': sols,
                        'total': total,
                        'amount': amount}

    return context_dict


@login_required
def get_cart_detail(request):
    cust_id = Cust.objects.get(user_id=User.objects.get(username=request.user.username).id).id
    context_dict = get_cart_info(cust_id)
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
    logger.debug('创建订单行#' + str(sol.id))
    qty = sol.qty
    amount = int(sol.qty) * prod.price
    context_dict = get_cart_info(cust_id)
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
    logger.debug('创建订单行#' + str(sol.id))
    qty = sol.qty
    amount = int(sol.qty) * prod.price
    context_dict = get_cart_info(cust_id)
    return render(request,
                  'ec/_cart_detail.html',
                  context_dict)


@login_required
def rmv_prod(request):
    cust_id = Cust.objects.get(user_id=User.objects.get(username=request.user.username).id).id
    so_id = create_order(cust_id)
    prod = Prod.objects.get(id=request.POST.get('prod_id'))
    cnt_so_prod = Sol.objects.filter(cust_id=cust_id,
                                     so_id=so_id).count()
    cnt_prod = Sol.objects.filter(cust_id=cust_id,
                                  so_id=so_id,
                                  prod_id=prod.id).count()
    # No select distinct prod_id
    # cnt_so_prod = Sol.objects.filter(cust_id=cust_id,
    #                                  so_id=so_id).values('prod_id').distinct().annotate(count=Count())[0]['count']
    print cnt_so_prod
    logger.debug('订单#' + str(so_id) + '商品distinct数:' + str(cnt_so_prod))
    if cnt_so_prod == cnt_prod:
        # 购物车只有一种商品时，在移除该商品的同时需要删除订单信息
        # Sol.objects.filter(cust_id=cust_id,
        #                    so_id=so_id,
        #                    prod_id=prod.id,
        #                    status=1).delete()
        Sol.objects.filter(cust_id=cust_id,
                           so_id=so_id,
                           status=1).delete()
        logger.debug('删除商品#' + str(prod.id) + '订单行')
        So.objects.get(id=so_id).delete()
        logger.debug('删除商品#' + str(prod.id) + '所在订单#' + str(so_id))
    else:
        Sol.objects.filter(cust_id=cust_id,
                           so_id=so_id,
                           prod_id=prod.id,
                           status=1).delete()
        logger.debug('删除商品#' + str(prod.id) + '订单行')
    context_dict = get_cart_info(cust_id)
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
    # 查询客户订单信息
    so = So.objects.filter(cust_id=cust.id, status=1)[0]
    # 修改客户订单的地址信息
    so.province = request.POST.get('province')
    so.city = request.POST.get('city')
    so.country = request.POST.get('area')
    so.address = request.POST.get('detailAddress')
    # 聚合购物车商品总数
    total = Sol.objects.filter(cust_id=cust.id,
                               status=1).values('so_id').annotate(total=Sum(F('qty')))[0]['total']
    # 聚合购物车商品总额
    amount = Sol.objects.filter(cust_id=cust.id,
                                status=1).values('so_id').annotate(amount=Sum(F('qty') * F('price')))[0]['amount']
    so.total = total
    so.amount = amount
    # 修改客户订单的状态
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
        'cust': cust,
        'so_number': so.id
    }
    return render(request,
                  'ec/checkout_confirm.html',
                  context_dict)


@login_required
def get_order_list(request):
    cust = Cust.objects.get(user_id=User.objects.get(username=request.user.username).id)
    # 查询该用户是否有订单信息
    cnt = So.objects.filter(cust_id=cust.id, status=888).annotate(cnt=Count('id'))
    if len(cnt) == 0:
        context_dict = {'cnt': 0,
                        'cust': cust}
    else:
        # 查询客户订单信息
        sos = So.objects.filter(cust_id=cust.id, status=888).order_by('-id')
        context_dict = {'cust': cust,
                        'sos': sos}
    return render(request,
                  'ec/order_list.html',
                  context_dict)


def get_order_info(so_id):
    # 对订单行信息进行展示聚合
    so = So.objects.get(id=so_id)
    sols = Sol.objects.filter(so_id=so_id,
                              status=888).values('so_id',
                                                 'prod_id',
                                                 'name',
                                                 'img_t',
                                                 'price').annotate(qty=Sum('qty'),
                                                                   amt=Sum('qty') * F('price'))
    # 20170112之前因为在checkout confirm时没有更新订单商品总数、总金额，在查看时用如下代码做订单信息更新
    # 聚合购物车商品总数
    # total = Sol.objects.filter(so_id=so_id,
    #                            status=888).values('so_id').annotate(total=Sum(F('qty')))[0]['total']
    # so.total = total

    # 聚合购物车商品总额
    # amount = Sol.objects.filter(so_id=so_id,
    #                             status=888).values('so_id').annotate(amount=Sum(F('qty') * F('price')))[0]['amount']
    # so.amount = amount
    # so.save()
    # 20170112之前仅仅是返回商品总数和总金额，20170112之后返回全部订单信息包括订单商品总数、总金额以及收件人、收货地址信息
    # total = so.total
    # amount = so.amount
    logger.debug('查询用户订单行信息')
    context_dict = {'so': so,
                    'sols': sols}
    return context_dict


@login_required
def get_order_detail(request, so_id):
    context_dict = get_order_info(so_id)
    return render(request,
                  'ec/order_detail.html',
                  context_dict)
