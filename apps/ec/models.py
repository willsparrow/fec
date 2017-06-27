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
    status = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    created_date = models.DateTimeField(null=True)
    updated_date = models.DateTimeField(null=True)


class ProdPv(models.Model):
    class Meta:
        db_table = 't_prod_pv'
    prod_id = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    property_id = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    property_name = models.CharField(max_length=100, null=True)
    value = models.CharField(max_length=100, null=True)
    img_url = models.CharField(max_length=100, null=True)
    status = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    created_date = models.DateTimeField(null=True)
    updated_date = models.DateTimeField(null=True)


class Sku(models.Model):
    class Meta:
        db_table = 't_sku'
    prod_id = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    code = models.CharField(max_length=100, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    qty = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    img_url = models.CharField(max_length=100, null=True)
    pv = models.CharField(max_length=1000, null=True)
    status = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    created_date = models.DateTimeField(null=True)
    updated_date = models.DateTimeField(null=True)


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
    cust_id = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    prod_id = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    name = models.CharField(max_length=100, null=True)
    img_url = models.CharField(max_length=100, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    qty = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    created_date = models.DateTimeField(null=True)
    updated_date = models.DateTimeField(null=True)
    status = models.DecimalField(max_digits=10, decimal_places=0, null=True)

    def __str__(self):
        return str(self.id)


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
    status = models.CharField(max_length=100, null=True)
    created_date = models.DateTimeField(null=True)
    updated_date = models.DateTimeField(null=True)
    expire_date = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.id)
