# -*- coding: utf8 -*-
# Copyright (C) 2017, www.meibailian.com

# FEC
from .models import *


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

