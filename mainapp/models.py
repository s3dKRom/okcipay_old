from django.db import models

# Create your models here.
class Accounts(models.Model):
    class Meta():
        db_table = 'accounts'
    number = models.CharField(max_length=14)
    currency = models.DecimalField(max_digits=3, decimal_places=0)
    locked_out = models.BooleanField()

class Users(models.Model):
    class Meta():
        db_table = 'users'
    code = models.CharField(max_length=10)
    password = models.CharField(max_length=128)
    title = models.CharField(max_length=80)
    locked_out = models.BooleanField()

class Balances(models.Model):
    class Meta():
        db_table = 'balances'
    id_account = models.ForeignKey(Accounts)
    dt = models.TextField()
    balance = models.DecimalField(max_digits=16, decimal_places=0)

class Users_Accounts(models.Model):
    class Meta():
        db_table = 'users_accounts'
    id_client = models.ForeignKey(Users)
    id_account = models.ForeignKey(Accounts)
    card_number = models.CharField(max_length=14)
    access_mode = models.BooleanField()


class Documents(models.Model):
    class Meta():
        db_table = 'documents'
    id_account = models.ForeignKey(Accounts)
    dt = models.TextField()
    dt_bank = models.TextField()
    docnum = models.CharField(max_length=10)
    code_bank_a = models.DecimalField(max_digits=9, decimal_places=0)
    account_a = models.DecimalField(max_digits=14, decimal_places=0)
    client_a = models.CharField(max_length=38)
    ident_a = models.CharField(max_length=10)
    code_bank_b = models.DecimalField(max_digits=9, decimal_places=0)
    account_b = models.DecimalField(max_digits=14, decimal_places=0)
    client_b = models.CharField(max_length=38)
    ident_b = models.CharField(max_length=10)
    debit_credit = models.BooleanField()
    kind = models.DecimalField(max_digits=2, decimal_places=0, null=True)
    amount = models.DecimalField(max_digits=16, decimal_places=0, null=True)
    purpose = models.TextField()
    amount_nv = models.DecimalField(max_digits=16, decimal_places=0, null=True)

class Currencies(models.Model):
    class Meta():
        db_table = 'currencies'
    code_currency = models.DecimalField(max_digits=3, decimal_places=0)
    currency_int = models.TextField()
    currency_loc = models.TextField()

class Banks(models.Model):
    class Meta():
        db_table = 'banks'
    code_bank = models.DecimalField(max_digits=6, decimal_places=0)
    bank_name = models.TextField()
