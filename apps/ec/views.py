# -*- coding: utf8 -*-
# Copyright (C) 2017, www.meibailian.com

import logging
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import *
from .forms import *
from django.db.models import Sum
from django.db.models import Count
from django.db.models import F
from django.db import transaction
# MNS
from libs.mns.mns_python_sdk.mns.account import Account
from libs.mns.mns_python_sdk.mns.topic import *
from fec import mns
# qrcode
import qrcode
from django.utils.six import BytesIO
# wxpay
from .wxpay import *
# CSRF
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

logger = logging.getLogger('django')


def send_orderid_to_shopkeeper_by_sms(shopkeeper, order_id):
    access_key_id = mns.AccessKeyId
    access_key_secret = mns.AccessKeySecret
    endpoint = mns.Endpoint
    topic = mns.Topic
    sign_name = mns.SignName
    template_code_for_shopkeeper = mns.TemplateCodeForShopkeeper

    my_account = Account(endpoint, access_key_id, access_key_secret)
    my_topic = my_account.get_topic(topic)
    msg_body1 = "sms-message1."
    direct_sms_attr1 = DirectSMSInfo(free_sign_name=sign_name, template_code=template_code_for_shopkeeper, single=False)
    direct_sms_attr1.add_receiver(receiver=shopkeeper, params={"order_id": str(order_id)})
    msg1 = TopicMessage(msg_body1, direct_sms=direct_sms_attr1)
    try:
        re_msg = my_topic.publish_message(msg1)
        sms_log = SmsLog()
        sms_log.order_id = order_id
        sms_log.receiver = shopkeeper
        sms_log.type = 'orderNotifyToShopkeeper'
        sms_log.message_id = re_msg.message_id
        sms_log.created_date = timezone.now()
        sms_log.updated_date = timezone.now()
        sms_log.save()
        logger.debug("Publish Message Succeed. MessageBody:%s MessageID:%s" % (msg_body1, re_msg.message_id))
    except MNSExceptionBase, e:
        if e.type == "TopicNotExist":
            logger.debug("Topic not exist, please create it.")
        logger.debug("Publish Message Fail. Exception:%s" % e)


def index(request):
    return render(request, 'ec/index.html')


# 查询所有商品信息
def get_prod_list(request):
    # prods = Prod.objects.all()
    prods = Prod.objects.filter(status=1)
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


# 根据商品关键字查询该类型所有商品信息
def get_prod_list_by_keywords(request):
    keywords = request.GET.get('keywords')
    cnt = Prod.objects.filter(keywords__contains=keywords).count()
    if cnt == 0:
        context_dict = {'cnt': 0}
    else:
        prods = Prod.objects.filter(keywords__contains=keywords)
        logger.debug('根据商品关键字' + keywords.encode('utf-8') + '查询该类型所有商品信息')
        logger.debug(prods)
        add_to_cart_form = AddToCartForm(initial={'qty': 1})
        context_dict = {'prods': prods,
                        'add_to_cart_form': add_to_cart_form}
    return render(request,
                  'ec/prod_list.html',
                  context_dict)


def get_prod_thumb_imgs(prod_id):
    cnt = ProdThumb.objects.filter(prod_id=prod_id).count()
    if cnt == 0:
        prod_thumbs = 0
    else:
        prod_thumbs = ProdThumb.objects.filter(prod_id=prod_id)
    return prod_thumbs


def get_prod_detail_imgs(prod_id):
    cnt = ProdDetail.objects.filter(prod_id=prod_id).count()
    if cnt == 0:
        prod_details = 0
    else:
        prod_details = ProdDetail.objects.filter(prod_id=prod_id)
    return prod_details


def get_prod_properties(prod_id):
    cnt = ProdProperty.objects.filter(prod_id=prod_id).count()
    if cnt == 0:
        properties = 0
    else:
        properties = ProdProperty.objects.filter(prod_id=prod_id)
    return properties


def get_prod_property_values(property_id):
    cnt = ProdPv.objects.filter(property_id=property_id).count()
    if cnt == 0:
        values = 0
    else:
        values = ProdPv.objects.filter(property_id=property_id)
    return values


def get_prod_pvs(prod_id):
    property_list = []
    properties = get_prod_properties(prod_id)
    if properties != 0:
        for property in properties:
            property_dict={}
            property_dict['id'] = property.id
            property_dict['name'] = property.name
            property_dict['values'] = get_prod_property_values(property.id)
            property_list.append(property_dict)
        return property_list
    else:
        return 0


def get_prod_pvs_json(request, prod_id):
    prod_id = int(prod_id)
    property_list = []
    properties = get_prod_properties(prod_id)
    if properties != 0:
        for property in properties:
            property_dict = {}
            property_dict['id'] = int(property.id)
            property_dict['name'] = property.name
            property_dict['selected_value'] = None
            values = []
            property_values = get_prod_property_values(property.id)
            for property_value in property_values:
                value ={}
                value['id'] = int(property_value.id)
                value['property_id'] = int(property_value.property_id)
                value['value'] = property_value.value
                value['img_url'] = property_value.img_url
                values.append(value)
            property_dict['values'] = values
            property_list.append(property_dict)
        return HttpResponse(json.dumps(property_list))
    else:
        return HttpResponse(0)


def get_prod_skus_json(request, prod_id):
    logger.debug("查询prod#" + str(prod_id) + "的sku json")
    cnt = Sku.objects.filter(prod_id=prod_id).count()
    if cnt != 0:
        skus = Sku.objects.filter(prod_id=prod_id)
        sku_list = []
        for sku in skus:
            sku_dict = {}
            sku_dict['id'] = sku.id
            sku_dict['prod_id'] = int(sku.prod_id)
            sku_dict['price'] = str(sku.price)
            sku_dict['qty'] = int(sku.qty)
            sku_dict['pvs'] = sku.pvs
            sku_list.append(sku_dict)
        return HttpResponse(json.dumps(sku_list))
    else:
        return HttpResponse(0)


# 查询某个商品的详情信息
def get_prod_detail(request, prod_id):
    prod = Prod.objects.get(id=prod_id)
    add_to_cart_form = AddToCartForm(initial={'qty': 1})
    prod_details = get_prod_detail_imgs(prod_id)
    prod_thumbs = get_prod_thumb_imgs(prod_id)
    prod_pvs = get_prod_pvs(prod_id)
    context_dict = {'prod': prod,
                    'prod_details': prod_details,
                    'prod_thumbs': prod_thumbs,
                    'prod_pvs': prod_pvs,
                    'add_to_cart_form': add_to_cart_form}
    return render(request,
                  'ec/prod_detail.html',
                  context_dict)


# 创建订单
def create_order(cust_id):
    logger.debug('查询该客户是否有未处理的订单')
    cnt = So.objects.filter(cust_id=cust_id, status=1).count()
    logger.debug(cnt)
    if cnt == 0:
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
    prod_id = request.POST.get('prod_id')
    qty = request.POST.get('qty')
    prod = Prod.objects.get(id=prod_id)
    amount = int(qty) * prod.price
    # check库存
    if prod.qty < int(qty):
        enough = 0
    else:
        enough = 1
        # 创建订单
        so_id = create_order(cust_id)
        # 创建订单行
        sol = Sol()
        sol.so_id = so_id
        sol.cust_id = cust_id
        sol.prod_id = prod.id
        sol.name = prod.name
        sol.img_url = prod.img_url
        sol.price = prod.price
        sol.qty = qty
        sol.created_date = timezone.now()
        sol.updated_date = timezone.now()
        sol.status = 1
        sol.save()
        logger.debug('创建订单行#' + str(sol.id))
        qty = sol.qty
        amount = int(sol.qty) * prod.price
    context_dict = {'prod': prod,
                    'qty': qty,
                    'enough': enough,
                    'amount': amount}
    return render(request,
                  'ec/_add_to_cart_message.html',
                  context_dict)


@login_required
def add_sku_to_cart(request):
    cust_id = Cust.objects.get(user_id=User.objects.get(username=request.user.username).id).id
    prod_id = request.POST.get('prod_id')
    sku_id = request.POST.get('sku_id')
    qty = request.POST.get('qty')
    print(prod_id)
    print(sku_id)
    print(qty)
    prod = Prod.objects.get(id=prod_id)
    sku = Sku.objects.get(id=sku_id)
    amount = int(qty) * sku.price
    # check库存
    if sku.qty < int(qty):
        enough = 0
    else:
        enough = 1
        # 创建订单
        so_id = create_order(cust_id)
        # 创建订单行
        sol = Sol()
        sol.so_id = so_id
        sol.cust_id = cust_id
        sol.prod_id = prod.id
        sol.sku_id = sku.id
        sol.name = sku.name
        sol.img_url = sku.img_url
        sol.price = sku.price
        sol.qty = qty
        sol.created_date = timezone.now()
        sol.updated_date = timezone.now()
        sol.status = 1
        sol.description = sku.description
        sol.save()
        logger.debug('创建订单行#' + str(sol.id))
        qty = sol.qty
        amount = int(sol.qty) * prod.price
    context_dict = {'sku': sku,
                    'qty': qty,
                    'enough': enough,
                    'amount': amount}
    return render(request,
                  'ec/_add_to_cart_message.html',
                  context_dict)


def get_cart_info(cust_id):
    # 查询该用户是否有购物车信息
    cust = Cust.objects.get(id=cust_id)
    cnt = So.objects.filter(cust_id=cust_id, status=1).count()
    if cnt == 0:
        context_dict = {'cnt': 0,
                        'cust': cust}
    else:
        # 对明细进行购物车展示聚合
        sols = Sol.objects.filter(cust_id=cust_id,
                                  status=1).values('so_id',
                                                   'prod_id',
                                                   'sku_id',
                                                   'name',
                                                   'img_url',
                                                   'price',
                                                   'description').annotate(qty=Sum('qty'),
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
def add_sku(request):
    cust_id = Cust.objects.get(user_id=User.objects.get(username=request.user.username).id).id
    so_id = create_order(cust_id)
    prod = Prod.objects.get(id=request.POST.get('prod_id'))
    sku = Sku.objects.get(id=request.POST.get('sku_id'))
    # 创建订单行
    sol = Sol()
    sol.so_id = so_id
    sol.cust_id = cust_id
    sol.prod_id = prod.id
    sol.sku_id = sku.id
    sol.name = sku.name
    sol.img_url = sku.img_url
    sol.price = sku.price
    sol.qty = 1
    sol.created_date = timezone.now()
    sol.updated_date = timezone.now()
    sol.status = 1
    sol.description = sku.description
    sol.save()
    logger.debug('创建订单行#' + str(sol.id))
    qty = sol.qty
    amount = int(sol.qty) * prod.price
    context_dict = get_cart_info(cust_id)
    return render(request,
                  'ec/_cart_detail.html',
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
    sol.img_url = prod.img_url
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
def del_sku(request):
    cust_id = Cust.objects.get(user_id=User.objects.get(username=request.user.username).id).id
    so_id = create_order(cust_id)
    prod = Prod.objects.get(id=request.POST.get('prod_id'))
    sku = Sku.objects.get(id=request.POST.get('sku_id'))
    sol = Sol()
    sol.so_id = so_id
    sol.cust_id = cust_id
    sol.prod_id = prod.id
    sol.sku_id = sku.id
    sol.name = sku.name
    sol.img_url = sku.img_url
    sol.price = prod.price
    sol.qty = -1
    sol.created_date = timezone.now()
    sol.updated_date = timezone.now()
    sol.status = 1
    sol.description = sku.description
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
    sol.img_url = prod.img_url
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
def rmv_sku(request):
    cust_id = Cust.objects.get(user_id=User.objects.get(username=request.user.username).id).id
    so_id = create_order(cust_id)
    prod = Prod.objects.get(id=request.POST.get('prod_id'))
    sku = Sku.objects.get(id=request.POST.get('sku_id'))
    cnt_sol = Sol.objects.filter(cust_id=cust_id,
                                 so_id=so_id).count()
    cnt_sol_sku = Sol.objects.filter(cust_id=cust_id,
                                     so_id=so_id,
                                     sku_id=sku.id).count()
    # No select distinct prod_id
    # cnt_so_prod = Sol.objects.filter(cust_id=cust_id,
    #                                  so_id=so_id).values('prod_id').distinct().annotate(count=Count())[0]['count']
    logger.debug('订单#' + str(so_id) + 'sku distinct数:' + str(cnt_sol_sku))
    if cnt_sol == cnt_sol_sku:
        # 购物车只有一种商品时，在移除该商品的同时需要删除订单信息
        # Sol.objects.filter(cust_id=cust_id,
        #                    so_id=so_id,
        #                    prod_id=prod.id,
        #                    status=1).delete()
        Sol.objects.filter(cust_id=cust_id,
                           so_id=so_id,
                           status=1).delete()
        logger.debug('删除sku#' + str(sku.id) + '订单行')
        So.objects.get(id=so_id).delete()
        logger.debug('删除sku#' + str(sku.id) + '所在订单#' + str(so_id))
    else:
        Sol.objects.filter(cust_id=cust_id,
                           so_id=so_id,
                           prod_id=prod.id,
                           sku_id=sku.id,
                           status=1).delete()
        logger.debug('删除sku#' + str(sku.id) + '订单行')
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


@transaction.atomic
def deduct_stock(so_id):
    # 根据订单id对订单行在产品维度进行聚合
    sols = Sol.objects.filter(so_id=so_id,
                              status=1).values('so_id',
                                               'prod_id',
                                               'name',
                                               'img_url',
                                               'price').annotate(qty=Sum('qty'),
                                                                 amt=Sum('qty') * F('price'))
    # 根据订单上经过聚合的商品进行扣库存操作
    # 锁库存
    for sol in sols:
        Prod.objects.select_for_update().get(id=sol['prod_id'])
    # check库存
    # 缺货商品列表
    prods = []
    for sol in sols:
        prod = Prod.objects.select_for_update().get(id=sol['prod_id'])
        if prod.qty < sol['qty']:
            prods.append(prod)
    # 扣库存
    if len(prods) > 0:
        context_dict = {
            'success': 0,
            'prods': prods
        }
    else:
        for sol in sols:
            prod = Prod.objects.select_for_update().get(id=sol['prod_id'])
            prod.qty = prod.qty - sol['qty']
            prod.save()
        context_dict = {
            'success': 1
        }
    return context_dict


@transaction.atomic
def deduct_sku_stock(so_id):
    # 根据订单id对订单行在产品维度进行聚合
    sols = Sol.objects.filter(so_id=so_id,
                              status=1).values('so_id',
                                               'prod_id',
                                               'sku_id',
                                               'name',
                                               'img_url',
                                               'price').annotate(qty=Sum('qty'),
                                                                 amt=Sum('qty') * F('price'))
    # 根据订单上经过聚合的商品进行扣库存操作
    # 锁库存
    for sol in sols:
        Sku.objects.select_for_update().get(id=sol['sku_id'])
    # check库存
    # 缺货商品列表
    skus = []
    for sol in sols:
        sku = Sku.objects.select_for_update().get(id=sol['sku_id'])
        if sku.qty < sol['qty']:
            skus.append(sku)
    # 扣库存
    if len(skus) > 0:
        context_dict = {
            'success': 0,
            'skus': skus
        }
    else:
        for sol in sols:
            skus = Sku.objects.select_for_update().get(id=sol['sku_id'])
            sku.qty = sku.qty - sol['qty']
            sku.save()
        context_dict = {
            'success': 1
        }
    return context_dict


@login_required
def checkout_confirm(request):
    # 查询客户信息
    cust = Cust.objects.get(user_id=User.objects.get(username=request.user.username).id)
    # 修改客户的默认地址
    cust.province = request.POST.get('province')
    cust.city = request.POST.get('city')
    cust.country = request.POST.get('area')
    cust.address = request.POST.get('detailAddress')
    cust.save()
    # 查询客户订单信息
    so = So.objects.filter(cust_id=cust.id, status=1)[0]
    context_dict = deduct_sku_stock(so.id)
    # 扣库存成功
    if context_dict['success'] == 1:
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
        # 修改客户订单的商品总数和商品总额
        so.total = total
        so.amount = amount
        # 修改客户订单的状态
        so.status = 888
        so.save()
        # 查询客户订单对应的订单行信息
        sols = Sol.objects.filter(cust_id=cust.id,
                                  so_id=so.id,
                                  status=1)
        # 修改客户订单对应的订单行的状态
        for sol in sols:
            sol.status = 888
            sol.save()
        context_dict = {
            'cust': cust,
            'so_number': so.id
        }
        # 短信通知店员有新的订单生成
        send_orderid_to_shopkeeper_by_sms('18621101150', so.id)
        # send_orderid_to_shopkeeper_by_sms('15035048663', so.id)
        return render(request,
                      'ec/checkout_confirm.html',
                      context_dict)
    else:
        # 扣库存失败
        return render(request,
                      'ec/checkout_lack.html',
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
                                                 'img_url',
                                                 'price',
                                                 'description').annotate(qty=Sum('qty'),
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
    dict_so = {}
    dict_so['id'] = so.id
    dict_so['created_date'] = str(so.created_date)
    dict_so['total'] = str(so.total)
    dict_so['amount'] = str(so.amount)
    list_sols = []
    for sol in sols:
        dict_sol = {}
        dict_sol['so_id'] = str(sol['so_id'])
        dict_sol['prod_id'] = str(sol['prod_id'])
        dict_sol['name'] = sol['name']
        dict_sol['qty'] = str(sol['qty'])
        dict_sol['price'] = str(sol['price'])
        dict_sol['amt'] = str(sol['amt'])
        list_sols.append(dict_sol)
    logger.debug('查询用户订单行信息')
    context_dict = {'so': so,
                    'sols': sols,
                    'json_so': json.dumps(dict_so),
                    'json_sols': json.dumps(list_sols)}
    return context_dict


@login_required
def get_order_detail(request, so_id):
    context_dict = get_order_info(so_id)
    return render(request,
                  'ec/order_detail.html',
                  context_dict)


@login_required
def wxpay(request):
    so = So.objects.get(id=167)
    context_dict = {'so': so}
    return render(request,
                  'ec/wxpay.html',
                  context_dict)


@login_required
def generate_wxpay_qrcode(request, order_id):
    img = qrcode.make(unifiedorder(order_id))
    buf = BytesIO()
    img.save(buf)
    image_stream = buf.getvalue()
    response = HttpResponse(image_stream, content_type="image/png")
    return response


@csrf_exempt
def wxpay_callback(request):
    print request.body
    xml = unifiedorder_callback(xml=request.body)
    return HttpResponse(xml)


def xml(request):
    xml='''
<xml>
  <return_code><![CDATA[SUCCESS]]></return_code>
  <return_msg><![CDATA[OK]]></return_msg>
</xml>'''
    return HttpResponse(xml)


@csrf_exempt
def xml_post(request):
    print request.body
    return HttpResponse(0)

