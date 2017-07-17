# -*- coding: utf8 -*-
# Copyright (C) 2017, www.meibailian.com


from django.utils import timezone
from libs.pay.wxpay import *
from .models import So, WXPayLog, WXPayQrcode, WXPayResult
from fec import wxpay_settings


def unifiedorder(so_id):
    """发起微信支付统一下单请求
    @:param
    @:return string: qrcode img url
    """
    so = So.objects.get(id=so_id)
    wxpay_request_dict = {}
    wxpay_request_dict['appid'] = wxpay_settings.appid
    wxpay_request_dict['mch_id'] = wxpay_settings.mch_id
    wxpay_request_dict['nonce_str'] = ''
    wxpay_request_dict['sign'] = ''
    wxpay_request_dict['body'] = '美百联-在线支付'
    wxpay_request_dict['out_trade_no'] = so.id
    wxpay_request_dict['total_fee'] = int(so.amount * 100)
    wxpay_request_dict['spbill_create_ip'] = '115.29.239.5'
    wxpay_request_dict['notify_url'] = 'http://www.meibailian.com/wxpay_callback'
    wxpay_request_dict['trade_type'] = 'NATIVE'
    wxpay = WXPay(app_id=wxpay_settings.appid,
                  mch_id=wxpay_settings.mch_id,
                  key=wxpay_settings.key,
                  cert_pem_path=None,
                  key_pem_path=None)
    wxpay_request_dict = wxpay.fill_request_data(wxpay_request_dict)
    wxpay_log = WXPayLog()
    wxpay_log.so_id = so.id
    wxpay_log.appid = wxpay_request_dict['appid']
    wxpay_log.mch_id = wxpay_request_dict['mch_id']
    wxpay_log.nonce_str = wxpay_request_dict['nonce_str']
    wxpay_log.sign = wxpay_request_dict['sign']
    wxpay_log.body = wxpay_request_dict['body']
    wxpay_log.out_trade_no = wxpay_request_dict['out_trade_no']
    wxpay_log.total_fee = wxpay_request_dict['total_fee']
    wxpay_log.spbill_create_ip = wxpay_request_dict['spbill_create_ip']
    wxpay_log.notify_url = wxpay_request_dict['notify_url']
    wxpay_log.trade_type = wxpay_request_dict['trade_type']
    wxpay_log.created_date = timezone.now()
    wxpay_log.updated_date = timezone.now()
    wxpay_log.status = 1
    wxpay_log.save()
    # 处理微信支付统一接口请求结果
    try:
        resp_dict = wxpay.unifiedorder(wxpay_request_dict)
        wxpay_qrcode = WXPayQrcode()
        wxpay_qrcode.so_id = so.id
        wxpay_qrcode.appid = resp_dict['appid']
        wxpay_qrcode.mch_id = resp_dict['mch_id']
        wxpay_qrcode.nonce_str = resp_dict['nonce_str']
        wxpay_qrcode.sign = resp_dict['sign']
        wxpay_qrcode.sign_type = 'MD5'
        wxpay_qrcode.result_code = resp_dict['result_code']
        wxpay_qrcode.trade_type = resp_dict['trade_type']
        wxpay_qrcode.prepay_id = resp_dict['prepay_id']
        wxpay_qrcode.code_url = resp_dict['code_url']
        wxpay_qrcode.qrcode_url = 'http:/img.mbailian.com/wxpay_qrcode_' + str(wxpay_qrcode.so_id) + '.png'
        wxpay_qrcode.created_date = timezone.now()
        wxpay_qrcode.updated_date = timezone.now()
        wxpay_qrcode.status = 1
        wxpay_qrcode.save()
        return wxpay_qrcode.code_url
    except:
        print sys.exc_info()


def unifiedorder_callback(xml):
    """处理微信支付统一接口支付结果通知
    @:param
    @:return
    """
    wxpay_util = WXPayUtil()
    wxpay_result_dict = wxpay_util.xml2dict(xml)
    if wxpay_result_dict['return_code'] == 'SUCCESS':
        if wxpay_util.is_signature_valid(data=wxpay_result_dict, key=wxpay_settings.key):
            so = So.objects.get(id=wxpay_result_dict['out_trade_no'])
            if wxpay_result_dict['total_fee'] == int(so.amount * 100):
                cnt = WXPayResult.objects.filter(so_id=so.id).count()
                if cnt == 0:
                    wxpay_result = WXPayResult()
                    wxpay_result.so_id = so.id
                    wxpay_result.return_code = wxpay_result_dict['return_code']
                    wxpay_result.appid = wxpay_result_dict['appid']
                    wxpay_result.mch_id = wxpay_result_dict['mch_id']
                    wxpay_result.nonce_str = wxpay_result_dict['nonce_str']
                    wxpay_result.sign = wxpay_result_dict['sign']
                    wxpay_result.result_code = wxpay_result_dict['result_code']
                    wxpay_result.openid = wxpay_result_dict['openid']
                    wxpay_result.trade_type = wxpay_result_dict['trade_type']
                    wxpay_result.bank_type = wxpay_result_dict['bank_type']
                    wxpay_result.total_fee = wxpay_result_dict['total_fee']
                    wxpay_result.cash_fee = wxpay_result_dict['cash_fee']
                    wxpay_result.transaction_id = wxpay_result_dict['transaction_id']
                    wxpay_result.out_trade_no = wxpay_result_dict['out_trade_no']
                    wxpay_result.time_end = wxpay_result_dict['time_end']
                    wxpay_result.created_date = timezone.now()
                    wxpay_result.updated_date = timezone.now()
                    wxpay_result.status = 1
                    wxpay_callback_dict = {}
                    wxpay_callback_dict['return_code'] = 'SUCCESS'
                    xml = wxpay_util.dict2xml(wxpay_callback_dict)
                    return xml
    else:
        wxpay_callback_dict = {}
        wxpay_callback_dict['return_code'] = 'FAIL'
        xml = wxpay_util.dict2xml(wxpay_callback_dict)
        return xml

