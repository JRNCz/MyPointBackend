# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

import django.utils
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

# TODO : tostrings and verbose_name and verbose_name_plural

class ClientManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

    def _create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
class About(models.Model):
    feedback = models.OneToOneField('Feedback', models.DO_NOTHING, primary_key=True)
    asset = models.ForeignKey('Facility', models.DO_NOTHING, blank=True, null=True)
    objects = models.Manager()
    class Meta:
        managed = True
        db_table = 'about'


class Bus(models.Model):
    asset = models.ForeignKey('Facility', models.DO_NOTHING, blank=True, null=True)
    owner = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'bus'


class Busstop(models.Model):
    asset = models.ForeignKey('Facility', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'busstop'


class Carpark(models.Model):
    asset = models.ForeignKey('Facility', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'carpark'


class Client(AbstractUser):
    
    points = models.DecimalField(max_digits=10, decimal_places=0, default=0 , blank=True, null=True)
    reputation = models.DecimalField(max_digits=10, decimal_places=0, default = 0, blank=True, null=True)
    level = models.DecimalField(max_digits=10, decimal_places=0, default = 0, blank=True, null=True)

    
    def get_password (self, password):
       return self.password == password

    
    class Meta:
        managed = True
        db_table = 'client'
    
    objects = ClientManager()


class Facility(models.Model):
    
    asset_id = models.DecimalField(primary_key=True, max_digits=8, decimal_places=0)
    latitude = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    asset_name = models.CharField(max_length=50, blank=True, null=True)
    asset_type = models.CharField(max_length=25, blank=True, null=True)
    
    objects = models.Manager()
    
    class Meta:
        managed = True
        db_table = 'facility'
    


class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    feedback_type = models.CharField(max_length=20, blank=True, null=True)
    feedback_subtype = models.CharField(max_length=20, blank=True, null=True)
    time_action = models.DateTimeField(blank=True, null=True)
    score = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    image_data = models.BinaryField(blank=True, null=True)
    text = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'feedback'


class Item(models.Model):
    item_id = models.DecimalField(primary_key=True, max_digits=8, decimal_places=0)
    category = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    shop = models.ForeignKey('Shop', models.DO_NOTHING)
    valid = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'item'
        unique_together = (('item_id', 'shop'),)


class Mobilitystation(models.Model):
    asset = models.ForeignKey(Facility, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'mobilitystation'


class Opinates(models.Model):
    user = models.ForeignKey(Client, models.DO_NOTHING, blank=True, null=True)
    feedback = models.OneToOneField(Feedback, models.DO_NOTHING, primary_key=True)
    hashed_deviceid = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'opinates'


class Orders(models.Model):
    item = models.OneToOneField(Item, models.DO_NOTHING, primary_key=True)
    user = models.ForeignKey(Client, models.DO_NOTHING, blank=True, null=True)
    order_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'orders'


class Shop(models.Model):
    name = models.CharField(max_length=25, blank=True, null=True)
    shop_id = models.DecimalField(primary_key=True, max_digits=8, decimal_places=0)

    class Meta:
        managed = True
        db_table = 'shop'
