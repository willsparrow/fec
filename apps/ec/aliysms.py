# -*- coding: utf8 -*-
# Copyright (C) 2017, www.meibailian.com

import logging
from django.utils import timezone
# FEC
from .models import *
# SMS
from fec import settings_aliysms
import sys
from libs.sms.aliyunpythonsdkdysmsapi.aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from libs.sms.aliyunpythonsdkdysmsapi.aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
from aliyunsdkcore.client import AcsClient
import uuid
from aliyunsdkcore.profile import region_provider

logger = logging.getLogger('django')

"""
短信业务调用接口示例，版本号：v20170525

Created on 2017-06-12

"""

reload(sys)
sys.setdefaultencoding('utf8')

# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

# ACCESS_KEY_ID/ACCESS_KEY_SECRET 根据实际申请的账号信息进行替换
ACCESS_KEY_ID = settings_aliysms.AccessKeyId
ACCESS_KEY_SECRET = settings_aliysms.AccessKeySecret

acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)

SIGN_NAME = settings_aliysms.SignName
TEMPLATE_CODE_FOR_SHOPKEEPER = settings_aliysms.TemplateCodeForShopkeeper
TEMPLATE_CODE_FOR_REGISTER = settings_aliysms.TemplateCodeForRegister
TEMPLATE_CODE_FOR_RESET_PASSWORD = settings_aliysms.TemplateCodeForResetPassword

def send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):
    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)

    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)

    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)

    # 短信签名
    smsRequest.set_SignName(sign_name);

    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)

    # TODO 业务处理

    return smsResponse


def query_send_detail(biz_id, phone_number, page_size, current_page, send_date):
    queryRequest = QuerySendDetailsRequest.QuerySendDetailsRequest()
    # 查询的手机号码
    queryRequest.set_PhoneNumber(phone_number)
    # 可选 - 流水号
    queryRequest.set_BizId(biz_id)
    # 必填 - 发送日期 支持30天内记录查询，格式yyyyMMdd
    queryRequest.set_SendDate(send_date)
    # 必填-当前页码从1开始计数
    queryRequest.set_CurrentPage(current_page)
    # 必填-页大小
    queryRequest.set_PageSize(page_size)

    # 调用短信记录查询接口，返回json
    queryResponse = acs_client.do_action_with_exception(queryRequest)

    # TODO 业务处理

    return queryResponse

"""
__name__ = 'send'
if __name__ == 'send':
    __business_id = uuid.uuid1()
    print __business_id
    params = "{\"order_id\":\"12345\"}"
    print send_sms(__business_id, "18621101150", "美百联", "SMS_71045198", params)

if __name__ == 'query':
    print query_send_detail("1234567^8901234", "13000000000", 10, 1, "20170612")
"""


def send_orderid_to_shopkeeper_by_sms(shopkeeper, order_id):
    params = "{\"order_id\":\"" + str(order_id) + "\"}"
    __business_id = uuid.uuid1()
    msg = send_sms(__business_id, shopkeeper, SIGN_NAME, TEMPLATE_CODE_FOR_SHOPKEEPER, params)
    sms_log = SmsLog()
    sms_log.order_id = order_id
    sms_log.receiver = shopkeeper
    sms_log.type = 'orderNotifyToShopkeeper'
    sms_log.message_id = ''
    sms_log.message_content = msg
    sms_log.created_date = timezone.now()
    sms_log.updated_date = timezone.now()
    sms_log.save()
    logger.debug(msg)


def send_verifycode_for_reset_password(mobilephone, verifycode):
    params = "{\"code\":\"" + str(verifycode) + "\"}"
    __business_id = uuid.uuid1()
    logger.debug(mobilephone)
    msg = send_sms(__business_id, mobilephone, SIGN_NAME, TEMPLATE_CODE_FOR_RESET_PASSWORD, params)
    logger.debug(msg)
    sms_log = SmsLog()
    sms_log.receiver = mobilephone
    sms_log.type = 'verifyCodeToResetPassword'
    sms_log.message_id = ''
    sms_log.message_content = msg
    sms_log.created_date = timezone.now()
    sms_log.updated_date = timezone.now()
    sms_log.save()
    logger.debug(msg)


def send_verifycode_for_register(mobilephone, verifycode):
    params = "{\"code\":\"" + str(verifycode) + "\"}"
    __business_id = uuid.uuid1()
    msg = send_sms(__business_id, mobilephone, SIGN_NAME, TEMPLATE_CODE_FOR_REGISTER, params)
    sms_log = SmsLog()
    sms_log.receiver = mobilephone
    sms_log.type = 'verifyCodeToRegister'
    sms_log.message_id = ''
    sms_log.message_content = msg
    sms_log.created_date = timezone.now()
    sms_log.updated_date = timezone.now()
    sms_log.save()
    logger.debug(msg)

