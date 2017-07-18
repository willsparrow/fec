# -*- coding: utf8 -*-
# Copyright (C) 2017, www.meibailian.com

import logging
from django.utils import timezone
# FEC
from .models import *
# MNS
from libs.mns.mns_python_sdk.mns.account import Account
from libs.mns.mns_python_sdk.mns.topic import *
from fec import settings_mns


logger = logging.getLogger('django')


def send_orderid_to_shopkeeper_by_sms(shopkeeper, order_id):
    access_key_id = settings_mns.AccessKeyId
    access_key_secret = settings_mns.AccessKeySecret
    endpoint = settings_mns.Endpoint
    topic = settings_mns.Topic
    sign_name = settings_mns.SignName
    template_code_for_shopkeeper = settings_mns.TemplateCodeForShopkeeper

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