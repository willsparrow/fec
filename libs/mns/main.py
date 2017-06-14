# -*- coding: utf8 -*-
# Copyright (C) 2017, www.meibailian.com


import sys
import time
from libs.mns.mns_python_sdk.mns.account import Account
from libs.mns.mns_python_sdk.mns.queue import *
from libs.mns.mns_python_sdk.mns.topic import *
from libs.mns.mns_python_sdk.mns.subscription import *

import ConfigParser

'''
Step 1. 获取主题引用
'''
# 从https://account.console.aliyun.com/#/secure获取$YourAccountid
# 从https://ak-console.aliyun.com/#/accesskey获取$YourAccessId和$YourAccessKey
# 从http://$YourAccountId.mns.cn-hangzhou.aliyuncs.com获取$YourMNSEndpoint, eg. http://1234567890123456.mns.cn-hangzhou.aliyuncs.com
my_account = Account("https://1409889928667393.mns.cn-hangzhou.aliyuncs.com/", "LTAIRJSDbAUMLoOV", "5lqk46q3vz8c4I7I6AkNuj7y1Pse9N")
my_topic = my_account.get_topic("sms.topic-cn-hangzhou")
'''
Step 2. 设置SMS消息体（必须）
注：目前暂时不支持消息内容为空，需要指定消息内容，不为空即可。
'''
msg_body1 = "sms-message1."
'''
Step 3. 生成SMS消息属性，single=False表示每个接收者参数不一样，
'''
# 3.1 设置SMSSignName和SMSTempateCode
direct_sms_attr1 = DirectSMSInfo(free_sign_name="美百联", template_code="SMS_71045198", single=False)
# 3.2 指定接收短信的手机号并指定发送给该接收人的短信中的参数值（在短信模板中定义的）
direct_sms_attr1.add_receiver(receiver="18621101150", params={"order_id": "001"})
'''
#Step 5. 生成SMS消息对象
'''
msg1 = TopicMessage(msg_body1, direct_sms = direct_sms_attr1)
try:
    '''
    Step 6. 发布SMS消息
    '''
    re_msg = my_topic.publish_message(msg1)
    print "Publish Message Succeed. MessageBody:%s MessageID:%s" % (msg_body1, re_msg.message_id)
except MNSExceptionBase,e:
    if e.type == "TopicNotExist":
        print "Topic not exist, please create it."
        sys.exit(1)
    print "Publish Message Fail. Exception:%s" % e