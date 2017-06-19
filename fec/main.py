# -*- coding: utf8 -*-

from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import SetPasswordForm
from django.shortcuts import redirect
from apps.ec.models import Cust
from apps.ec.models import Md5
from apps.ec.models import SmsLog
from apps.ec.models import Verifycode
from django.db.models import Count
# MNS
from libs.mns.mns_python_sdk.mns.account import Account
from libs.mns.mns_python_sdk.mns.topic import *
import mns

import hashlib
import random
import datetime
import logging


# Create your views here.

logger = logging.getLogger('django')

def index(request):
    return render(request,
                  'fec/index.html')


@login_required
def test(request):
    return render(request,
                  'fec/pseudo-element-before-after.html')


def send_verifycode_to_mobilephone(mobilephone, template_code, description):
    access_key_id = mns.AccessKeyId
    access_key_secret = mns.AccessKeySecret
    endpoint = mns.Endpoint
    topic = mns.Topic
    sign_name = mns.SignName

    my_account = Account(endpoint, access_key_id, access_key_secret)
    my_topic = my_account.get_topic(topic)
    msg_body1 = "sms-message1."
    code = random.randint(100000, 999999)
    logger.debug(code)
    direct_sms_attr1 = DirectSMSInfo(free_sign_name=sign_name, template_code=template_code, single=False)
    direct_sms_attr1.add_receiver(receiver=mobilephone, params={"code": str(code)})
    msg1 = TopicMessage(msg_body1, direct_sms=direct_sms_attr1)
    try:
        verifycode = Verifycode()
        verifycode.mobilephone = mobilephone
        verifycode.verifycode = str(code)
        verifycode.status = 1
        verifycode.created_date = timezone.now()
        verifycode.updated_date = timezone.now()
        verifycode.expire_date = timezone.now() + datetime.timedelta(minutes=5)
        verifycode.save()

        re_msg = my_topic.publish_message(msg1)
        sms_log = SmsLog()
        sms_log.receiver = mobilephone
        sms_log.type = description
        sms_log.message_id = re_msg.message_id
        sms_log.created_date = timezone.now()
        sms_log.updated_date = timezone.now()
        sms_log.save()
        logger.debug("Publish Message Succeed. MessageBody:%s MessageID:%s" % (msg_body1, re_msg.message_id))
    except MNSExceptionBase, e:
        if e.type == "TopicNotExist":
            logger.debug("Topic not exist, please create it.")
        logger.debug("Publish Message Fail. Exception:%s" % e)


def validate_verifycode(mobilephone, verifycode):
    verifycode = Verifycode.objects.filter(mobilephone=mobilephone, verifycode=verifycode)
    if len(verifycode) == 1:
        if timezone.now() < verifycode[0].expire_date:
            return True
    else:
        return False


def register_step1(request):
    if request.method == 'POST':
        mobilephone = request.POST.get('mobilephone')
        exist = len(Cust.objects.filter(mobilephone=mobilephone).annotate(cnt=Count('mobilephone')))
        if exist == 1:
            context_dict = {'mobilephone': mobilephone,
                            'msg': '您输入的手机号码已被注册，如果忘记密码，请点击忘记密码进行密码找回。',
                            'exist': 1}
            return render(request,
                          'fec/register_step1.html',
                          context_dict)
        else:
            send_verifycode_to_mobilephone(mobilephone, mns.TemplateCodeForRegister, 'verifyCodeToRegister')
            context_dict = {'mobilephone': mobilephone,
                            'msg': '注册短信验证码已发送至您的手机，请填写手机验证码进行注册。'}
            return render(request,
                          'fec/register_step2.html',
                          context_dict)
    return render(request,
                  'fec/register_step1.html')


def register_step2(request):
    if request.method == 'POST':
        mobilephone = request.POST.get('mobilephone')
        verifycode = request.POST.get('verifycode')
        if validate_verifycode(mobilephone, verifycode):
            form = UserCreationForm()
            context_dict = {'mobilephone': mobilephone,
                            'form': form}
            return render(request,
                          'fec/register.html',
                          context_dict)
        else:
            context_dict = {'mobilephone': mobilephone,
                            'msg': '您输入的验证码不正确，请重新输入或重新注册。'}
            return render(request,
                          'fec/register_step2.html',
                          context_dict)


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        mobilephone = request.POST.get('mobilephone')
        form = UserCreationForm({'username': username,
                                 'password1': password1,
                                 'password2': password2})
        if form.is_valid():
            form.save()
            # 保存ec客户信息
            cust = Cust()
            cust.user_id = User.objects.get(username=username).id
            cust.name = username
            cust.mobilephone = mobilephone
            cust.created_date = timezone.now()
            cust.updated_date = timezone.now()
            cust.status = 1
            cust.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request,
                  'fec/register.html',
                  {'mobilephone': mobilephone,
                   'form': form})


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

def get_mobilephone_md5(mobilephone):
    exist = len(Md5.objects.filter(original=mobilephone).annotate(cnt=Count('original')))
    mobilephone_md5 = ''
    if exist == 0:
        mobilephone_md5 = hashlib.md5(mobilephone).hexdigest()
        md5 = Md5()
        md5.original = mobilephone
        md5.md5 = mobilephone_md5
        md5.created_date = timezone.now()
        md5.updated_date = timezone.now()
        md5.save()
    else:
        mobilephone_md5 = Md5.objects.get(original=mobilephone).md5
    return mobilephone_md5


def get_mobilephone_from_md5(md5):
    return Md5.objects.filter(md5=md5)[0].original


def send_verifycode(request):
    mobilephone = get_mobilephone_from_md5(request.POST.get('mobilephone'))
    send_verifycode_to_mobilephone(mobilephone, mns.TemplateCodeForResetPassword, 'verifyCodeToResetPassword')
    context_dict = {'msg': '已发送，请及时查收。'}
    return render(request,
                  'fec/_msg.html',
                  context_dict)


def reset_password_step1(request):
    return render(request,
                  'fec/reset_password_step1.html')


def reset_password_step2(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        cnt_username = len(User.objects.filter(username=username).annotate(cnt=Count('username')))
        cnt_mobilephone = len(Cust.objects.filter(mobilephone=username).annotate(cnt=Count('mobilephone')))
        cnt = cnt_username + cnt_mobilephone
        if cnt == 0:
            context_dict = {'cnt': 0,
                            'msg': '您输入的用户名/验证手机号不存在，请确认您输入无误。'}
            return render(request,
                          'fec/reset_password_step1.html',
                          context_dict)
        else:
            if cnt_username != 0:
                cust = Cust.objects.get(user_id=User.objects.get(username=username).id)
                mobilephone = cust.mobilephone
            else:
                mobilephone = username
            mobilephone_md5 = get_mobilephone_md5(mobilephone)
            context_dict = {'cnt': 1,
                            'mobilephone': mobilephone[0:3] + '*****' + mobilephone[-3:],
                            'mobilephone_md5': mobilephone_md5}
            return render(request,
                          'fec/reset_password_step2.html',
                          context_dict)


def reset_password_step3(request):
    if request.method == 'POST':
        logger.debug(request.POST.get('mobilephone', ''))
        logger.debug(request.POST.get('verifycode', ''))
        mobilephone = get_mobilephone_from_md5(request.POST.get('mobilephone', ''))
        verifycode = request.POST.get('verifycode', '')
        user_id = Cust.objects.filter(mobilephone=mobilephone)[0].user_id
        user = User.objects.get(id=user_id)
        logger.debug(mobilephone)
        logger.debug(verifycode)
        if validate_verifycode(mobilephone, verifycode):
            form = SetPasswordForm(user=user)
            return render(request,
                          'fec/reset_password_step3.html',
                          {'form': form,
                           'user_id': user_id})
    else:
        context_dict = {'msg': '验证码不正确！'}
        return render(request,
                      'fec/reset_password_step2.html',
                      context_dict)


def reset_password_step4(request):
    user_id = int(request.POST.get('user_id', ''))
    logger.debug(user_id)
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        new_password1 = request.POST.get('new_password1', '')
        new_password2 = request.POST.get('new_password2', '')
        form = SetPasswordForm(user,
                               {'new_password1': new_password1,
                                'new_password2': new_password2})
        if form.is_valid():
            form.save()
            logger.debug(user.username + ' password reset')
            return redirect('login')
    else:
        form = SetPasswordForm(user=user)
    return render(request,
                  'fec/reset_password_step3.html',
                  {'form': form,
                   'user_id':user_id})
