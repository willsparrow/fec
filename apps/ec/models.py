from django.db import models

# Create your models here.


class Prod(models.Model):
    class Meta:
        db_table = 't_prod'
    name = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=100, null=True)
    code = models.CharField(max_length=100, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    qty = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    unit = models.CharField(max_length=100, null=True)
    spec = models.CharField(max_length=100, null=True)
    created_date = models.DateTimeField(null=True)
    updated_date = models.DateTimeField(null=True)
    brand = models.CharField(max_length=100, null=True)
    company = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=100, null=True)
    status = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    img_url = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=1000, null=True)
    keywords = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.code


class ProdThumb(models.Model):
    class Meta:
        db_table = 't_prod_thumb'
    prod_id = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    img_url = models.CharField(max_length=100, null=True)
    seq = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    created_date = models.DateTimeField(null=True)
    updated_date = models.DateTimeField(null=True)


class ProdDetail(models.Model):
    class Meta:
        db_table = 't_prod_detail'
    prod_id = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    img_url = models.CharField(max_length=100, null=True)
    seq = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    created_date = models.DateTimeField(null=True)
    updated_date = models.DateTimeField(null=True)


class ProdProperty(models.Model):
    class Meta:
        db_table = 't_prod_property'
    prod_id = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    name = models.CharField(max_length=100, null=True)
    created_date = models.DateTimeField(null=True)
    updated_date = models.DateTimeField(null=True)
    status = models.DecimalField(max_digits=10, decimal_places=0, null=True)


class ProdPv(models.Model):
    class Meta:
        db_table = 't_prod_pv'
    prod_id = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    property_id = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    property_name = models.CharField(max_length=100, null=True)
    value = models.CharField(max_length=100, null=True)
    img_url = models.CharField(max_length=100, null=True)
    created_date = models.DateTimeField(null=True)
    updated_date = models.DateTimeField(null=True)
    status = models.DecimalField(max_digits=10, decimal_places=0, null=True)


class Sku(models.Model):
    class Meta:
        db_table = 't_sku'
    prod_id = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    name = models.CharField(max_length=100, null=True)
    code = models.CharField(max_length=100, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    qty = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    img_url = models.CharField(max_length=100, null=True)
    pvs = models.CharField(max_length=1000, null=True)
    description = models.CharField(max_length=1000, null=True)
    created_date = models.DateTimeField(null=True)
    updated_date = models.DateTimeField(null=True)
    status = models.DecimalField(max_digits=10, decimal_places=0, null=True)


class Cust(models.Model):
    class Meta:
        db_table = 't_cust'
    user_id = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    role = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100, null=True)
    birthday = models.DateTimeField(null=True)
    sex = models.CharField(max_length=100, null=True)
    photo = models.CharField(max_length=200, null=True)
    shop = models.CharField(max_length=100, null=True)
    company = models.CharField(max_length=100, null=True)
    mobilephone = models.CharField(max_length=100, null=True)
    telephone = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    province = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    created_date = models.DateTimeField(null=True)
    updated_date = models.DateTimeField(null=True)
    status = models.DecimalField(max_digits=10, decimal_places=0, null=True)

    def __str__(self):
        return str(self.id)


class So(models.Model):
    class Meta:
        db_table = 't_so'
    no = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    cust_id = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    cust_name = models.CharField(max_length=100, null=True)
    cust_mobilephone = models.CharField(max_length=100, null=True)
    cust_telephone = models.CharField(max_length=100, null=True)
    cust_email = models.CharField(max_length=100, null=True)
    shop = models.CharField(max_length=100, null=True)
    company = models.CharField(max_length=100, null=True)
    province = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    created_date = models.DateTimeField(null=True)
    updated_date = models.DateTimeField(null=True)
    status = models.DecimalField(max_digits=10, decimal_places=0, null=True)

    def __str__(self):
        return str(self.id)


class Sol(models.Model):
    class Meta:
        db_table = 't_sol'
    so_id = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    so_no = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    cust_id = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    prod_id = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    sku_id = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    name = models.CharField(max_length=100, null=True)
    img_url = models.CharField(max_length=100, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    qty = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    description = models.CharField(max_length=1000, null=True)
    created_date = models.DateTimeField(null=True)
    updated_date = models.DateTimeField(null=True)
    status = models.DecimalField(max_digits=10, decimal_places=0, null=True)


    def __str__(self):
        return str(self.id)


class WXPayLog(models.Model):
    class Meta:
        db_table = 't_wxpay_log'
    so_id = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    so_no = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    appid = models.CharField(max_length=100, null=True)
    mch_id = models.CharField(max_length=100, null=True)
    device_info = models.CharField(max_length=100, null=True)
    nonce_str = models.CharField(max_length=100, null=True)
    sign = models.CharField(max_length=100, null=True)
    sign_type = models.CharField(max_length=100, null=True)
    body = models.CharField(max_length=100, null=True)
    detail = models.CharField(max_length=10000, null=True)
    attach = models.CharField(max_length=200, null=True)
    out_trade_no = models.CharField(max_length=100, null=True)
    fee_type = models.CharField(max_length=100, null=True)
    total_fee = models.CharField(max_length=100, null=True)
    spbill_create_ip = models.CharField(max_length=100, null=True)
    notify_url = models.CharField(max_length=100, null=True)
    trade_type = models.CharField(max_length=100, null=True)
    openid = models.CharField(max_length=100, null=True)
    created_date = models.DateTimeField(null=True)
    updated_date = models.DateTimeField(null=True)
    status = models.DecimalField(max_digits=10, decimal_places=0, null=True)


class WXPayQrcode(models.Model):
    class Meta:
        db_table = 't_wxpay_qrcode'
    so_id = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    so_no = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    appid = models.CharField(max_length=100, null=True)
    mch_id = models.CharField(max_length=100, null=True)
    device_info = models.CharField(max_length=100, null=True)
    nonce_str = models.CharField(max_length=100, null=True)
    sign = models.CharField(max_length=100, null=True)
    sign_type = models.CharField(max_length=100, null=True)
    result_code = models.CharField(max_length=100, null=True)
    err_code = models.CharField(max_length=100, null=True)
    err_code_des = models.CharField(max_length=100, null=True)
    trade_type = models.CharField(max_length=100, null=True)
    prepay_id = models.CharField(max_length=100, null=True)
    code_url = models.CharField(max_length=100, null=True)
    created_date = models.DateTimeField(null=True)
    updated_date = models.DateTimeField(null=True)
    status = models.DecimalField(max_digits=10, decimal_places=0, null=True)



class WXPayMweb(models.Model):
    class Meta:
        db_table = 't_wxpay_mweb'
    so_id = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    so_no = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    appid = models.CharField(max_length=100, null=True)
    mch_id = models.CharField(max_length=100, null=True)
    device_info = models.CharField(max_length=100, null=True)
    nonce_str = models.CharField(max_length=100, null=True)
    sign = models.CharField(max_length=100, null=True)
    sign_type = models.CharField(max_length=100, null=True)
    result_code = models.CharField(max_length=100, null=True)
    err_code = models.CharField(max_length=100, null=True)
    err_code_des = models.CharField(max_length=100, null=True)
    trade_type = models.CharField(max_length=100, null=True)
    prepay_id = models.CharField(max_length=100, null=True)
    mweb_url = models.CharField(max_length=100, null=True)
    created_date = models.DateTimeField(null=True)
    updated_date = models.DateTimeField(null=True)
    status = models.DecimalField(max_digits=10, decimal_places=0, null=True)


class WXPayResult(models.Model):
    class Meta:
        db_table = 't_wxpay_result'
    so_id = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    so_no = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    return_code = models.CharField(max_length=100, null=True)
    return_msg = models.CharField(max_length=100, null=True)
    appid = models.CharField(max_length=100, null=True)
    mch_id = models.CharField(max_length=100, null=True)
    device_info = models.CharField(max_length=100, null=True)
    nonce_str = models.CharField(max_length=100, null=True)
    sign = models.CharField(max_length=100, null=True)
    sign_type = models.CharField(max_length=100, null=True)
    result_code = models.CharField(max_length=100, null=True)
    err_code = models.CharField(max_length=100, null=True)
    err_code_des = models.CharField(max_length=100, null=True)
    openid = models.CharField(max_length=200, null=True)
    is_subscribe = models.CharField(max_length=100, null=True)
    trade_type = models.CharField(max_length=100, null=True)
    bank_type = models.CharField(max_length=100, null=True)
    total_fee = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    fee_type = models.CharField(max_length=100, null=True)
    cash_fee = models.CharField(max_length=100, null=True)
    cash_fee_type = models.CharField(max_length=100, null=True)
    coupon_fee = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    coupon_count = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    transaction_id = models.CharField(max_length=100, null=True)
    out_trade_no = models.CharField(max_length=100, null=True)
    attach = models.CharField(max_length=200, null=True)
    time_end = models.CharField(max_length=100, null=True)
    created_date = models.DateTimeField(null=True)
    updated_date = models.DateTimeField(null=True)
    status = models.DecimalField(max_digits=10, decimal_places=0, null=True)


class SmsLog(models.Model):
    class Meta:
        db_table = 't_sms_log'
    order_id = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    receiver = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=100, null=True)
    message_id = models.CharField(max_length=100, null=True)
    created_date = models.DateTimeField(null=True)
    updated_date = models.DateTimeField(null=True)


class Md5(models.Model):
    class Meta:
        db_table = 't_md5'
    original = models.CharField(max_length=100, null=True)
    md5 = models.CharField(max_length=100, null=True)
    created_date = models.DateTimeField(null=True)
    updated_date = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.id)


class Verifycode(models.Model):
    class Meta:
        db_table = 't_verifycode'
    mobilephone = models.CharField(max_length=100, null=True)
    verifycode = models.CharField(max_length=100, null=True)
    created_date = models.DateTimeField(null=True)
    updated_date = models.DateTimeField(null=True)
    expire_date = models.DateTimeField(null=True)
    status = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)
