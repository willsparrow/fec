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
    img_l = models.CharField(max_length=200, null=True)
    img_m = models.CharField(max_length=200, null=True)
    img_s = models.CharField(max_length=200, null=True)
    img_t = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=1000, null=True)
    size = models.CharField(max_length=100, null=True)
    sex = models.CharField(max_length=100, null=True)
    color = models.CharField(max_length=100, null=True)
    weight = models.CharField(max_length=100, null=True)
    age = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.code


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
    img_t = models.CharField(max_length=100, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    qty = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    created_date = models.DateTimeField(null=True)
    updated_date = models.DateTimeField(null=True)
    status = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    def __str__(self):
        return str(self.id)
