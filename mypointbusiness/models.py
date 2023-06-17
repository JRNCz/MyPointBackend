# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from postgres_copy import CopyManager



class ClientManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
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



class Agency(models.Model):
    agency_id = models.TextField(primary_key=True)
    agency_name = models.TextField(blank=True, null=True)
    agency_url = models.TextField(blank=True, null=True)
    agency_timezone = models.TextField(blank=True, null=True)
    agency_lang = models.TextField(blank=True, null=True)
    agency_phone = models.TextField(blank=True, null=True)
    agency_fare_url = models.TextField(blank=True, null=True)
    agency_email = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'agency'

    objects = CopyManager()


class Bus(models.Model):
    facility = models.OneToOneField('Facility', models.DO_NOTHING, primary_key=True)
    unit_number = models.TextField(blank=True, null=True)
    registration_plate = models.TextField(blank=True, null=True)
    bus_desc = models.TextField(blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    standing_capacity = models.IntegerField(blank=True, null=True)
    seats = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'bus'


class Calendar(models.Model):
    service_id = models.TextField(primary_key=True)
    monday = models.BooleanField()
    tuesday = models.BooleanField()
    wednesday = models.BooleanField()
    thursday = models.BooleanField()
    friday = models.BooleanField()
    saturday = models.BooleanField()
    sunday = models.BooleanField()
    start_date = models.DecimalField(max_digits=8, decimal_places=0)
    end_date = models.DecimalField(max_digits=8, decimal_places=0)

    class Meta:
        managed = True
        db_table = 'calendar'


class CalendarDates(models.Model):
    service_id = models.TextField()
    date = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    exception_type = models.IntegerField(blank=True, null=True)
    calendar_dates_id = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'calendar_dates'


class Carpark(models.Model):
    name = models.TextField(blank=True, null=True)
    facility = models.OneToOneField('Facility', models.DO_NOTHING, primary_key=True)
    park_lat = models.FloatField()
    park_lon = models.FloatField()
    parking_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'carpark'





class Facility(models.Model):
    facility_id = models.TextField(primary_key=True, )

    class Meta:
        managed = True
        db_table = 'facility'


class Facilitytype(models.Model):
    facility_type_id = models.IntegerField(primary_key=True)
    facility_type_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True 
        db_table = 'facilitytype'


class FareAttributes(models.Model):
    fare_id = models.TextField(primary_key=True)
    price = models.FloatField()
    currency_type = models.TextField()
    payment_method = models.BooleanField()
    transfers = models.IntegerField(blank=True, null=True)
    transfer_duration = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True 
        db_table = 'fare_attributes'


class FareRules(models.Model):
    fare = models.OneToOneField(FareAttributes, models.DO_NOTHING, primary_key=True)
    route = models.ForeignKey('Routes', models.DO_NOTHING, blank=True, null=True)
    origin_id = models.TextField(blank=True, null=True)
    destination_id = models.TextField(blank=True, null=True)
    contains_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = True 
        db_table = 'fare_rules'


class FeedInfo(models.Model):
    feed_publisher_name = models.TextField(primary_key=True)
    feed_publisher_url = models.TextField()
    feed_lang = models.TextField(blank=True, null=True)
    feed_start_date = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    feed_end_date = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    feed_version = models.TextField(blank=True, null=True)
    feed_contact_email = models.TextField(blank=True, null=True)
    feed_contact_url = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'feed_info'


class Feedback(models.Model):
    user_lat = models.FloatField(blank=True, null=True)
    user_lon = models.FloatField(blank=True, null=True)
    feedback_category = models.CharField(max_length=50, blank=True, null=True)
    feedback_subcategory = models.CharField(max_length=50, blank=True, null=True)
    feedback_id = models.AutoField(primary_key=True)
    facility = models.ForeignKey(Facility, models.DO_NOTHING)
    time_action = models.DateTimeField()
    score = models.DecimalField(max_digits=2, decimal_places=1)
    image_url = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'feedback'
        unique_together = (('feedback_id', 'facility'),)


class Feedbackcat(models.Model):
    feedback_category = models.CharField(primary_key=True, max_length=50)
    feedback_category_short = models.CharField(max_length=50, blank=True, null=True)
    color_red = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    color_blue = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    color_green = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    imageurl = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'feedbackcat'


class Feedbackstruct(models.Model):
    feedback_struct_id = models.AutoField(primary_key=True)
    facility_type = models.ForeignKey(Facilitytype, models.DO_NOTHING, blank=True, null=True)
    feedback_category = models.ForeignKey(Feedbackcat, models.DO_NOTHING, db_column='feedback_category', blank=True, null=True)
    feedback_subcategory = models.ForeignKey('Feedbacksubcat', models.DO_NOTHING, db_column='feedback_subcategory', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'feedbackstruct'
        unique_together = (('facility_type', 'feedback_category', 'feedback_subcategory'),)


class Feedbacksubcat(models.Model):
    feedback_subcategory = models.CharField(primary_key=True, max_length=50)
    feedback_subcategory_short = models.CharField(max_length=50, blank=True, null=True)
    color_red = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    color_blue = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    color_green = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    imageurl = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'feedbacksubcat'


class Frequencies(models.Model):
    trip = models.ForeignKey('Trips', models.DO_NOTHING)
    start_time = models.DurationField()
    end_time = models.DurationField()
    headway_secs = models.IntegerField()
    exact_times = models.BooleanField(blank=True, null=True)
    frequency_id = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'frequencies'


class GiveFeedback(models.Model):
    give_feedback_id = models.AutoField(primary_key=True)
    feedback = models.OneToOneField(Feedback, models.DO_NOTHING, blank=True, null=True)
    facility_id = models.TextField(blank=True, null=True)
    user = models.ForeignKey(Client, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'give_feedback'


class HasFacilities(models.Model):
    has_facilities_id = models.AutoField(primary_key=True)
    facility_type = models.ForeignKey(Facilitytype, models.DO_NOTHING)
    facility = models.ForeignKey(Facility, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'has_facilities'
        unique_together = (('facility_type', 'facility'),)


class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=8, decimal_places=0)
    shop = models.ForeignKey('Shop', models.DO_NOTHING, blank=True, null=True)
    quantity = models.DecimalField(max_digits=1000, decimal_places=0)

    class Meta:
        managed = True
        db_table = 'item'
        unique_together = (('item_id', 'shop'),)


class Levels(models.Model):
    level_id = models.TextField(primary_key=True)
    level_index = models.FloatField()
    level_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'levels'


class Mobilitystation(models.Model):
    name = models.TextField(blank=True, null=True)
    facility = models.OneToOneField(Facility, models.DO_NOTHING, primary_key=True)
    mobility_lat = models.FloatField()
    mobility_lon = models.FloatField()

    class Meta:
        managed = True
        db_table = 'mobilitystation'


class Orders(models.Model):
    orders_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(Client, models.DO_NOTHING, blank=True, null=True)
    quantity = models.DecimalField(max_digits=2, decimal_places=0)
    order_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'orders'


class Pathways(models.Model):
    pathway_id = models.TextField(primary_key=True)
    from_stop = models.ForeignKey('Stops', models.DO_NOTHING, related_name='pathways_from_stop')
    to_stop = models.ForeignKey('Stops', models.DO_NOTHING, related_name='pathways_to_stop')
    pathway_mode = models.IntegerField()
    is_bidirectional = models.BooleanField()
    length = models.FloatField(blank=True, null=True)
    traversal_time = models.IntegerField(blank=True, null=True)
    stair_count = models.IntegerField(blank=True, null=True)
    max_slope = models.FloatField(blank=True, null=True)
    min_width = models.FloatField(blank=True, null=True)
    signposted_as = models.TextField(blank=True, null=True)
    reversed_signposted_as = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'pathways'


class Rail(models.Model):
    route = models.ForeignKey('Routes', models.DO_NOTHING, blank=True, null=True)
    facility = models.OneToOneField(Facility, models.DO_NOTHING, primary_key=True)
    agency_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'rail'


class Routes(models.Model):
    route_id = models.TextField(primary_key=True)
    agency = models.ForeignKey(Agency, models.DO_NOTHING, blank=True, null=True)
    route_short_name = models.TextField(blank=True, null=True)
    route_long_name = models.TextField(blank=True, null=True)
    route_desc = models.TextField(blank=True, null=True)
    route_type = models.IntegerField()
    route_url = models.TextField(blank=True, null=True)
    route_color = models.TextField(blank=True, null=True)
    route_text_color = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'routes'


class Shapes(models.Model):
    shpid = models.AutoField(primary_key=True)
    shape_id = models.TextField()
    shape_pt_lat = models.FloatField()
    shape_pt_lon = models.FloatField()
    shape_pt_sequence = models.IntegerField()
    shape_dist_traveled = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'shapes'


class Shop(models.Model):
    name = models.CharField(max_length=25, blank=True, null=True)
    shop_id = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'shop'


class StopTimes(models.Model):
    trip = models.ForeignKey('Trips', models.DO_NOTHING)
    arrival_time = models.DurationField(blank=True, null=True)
    departure_time = models.DurationField()
    stop = models.ForeignKey('Stops', models.DO_NOTHING)
    stop_sequence = models.IntegerField()
    stop_headsign = models.TextField(blank=True, null=True)
    pickup_type = models.IntegerField(blank=True, null=True)
    drop_off_type = models.IntegerField(blank=True, null=True)
    shape_dist_traveled = models.FloatField(blank=True, null=True)
    timepoint = models.BooleanField(blank=True, null=True)
    stop_times_id = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'stop_times'


class Stops(models.Model):
    stop = models.OneToOneField(Facility, models.DO_NOTHING, primary_key=True)
    stop_code = models.TextField(blank=True, null=True)
    stop_name = models.TextField(blank=True, null=True)
    stop_desc = models.TextField(blank=True, null=True)
    stop_lat = models.FloatField(blank=True, null=True)
    stop_lon = models.FloatField(blank=True, null=True)
    zone_id = models.TextField(blank=True, null=True)
    stop_url = models.TextField(blank=True, null=True)
    location_type = models.IntegerField(blank=True, null=True)
    parent_station = models.TextField(blank=True, null=True)
    stop_timezone = models.TextField(blank=True, null=True)
    wheelchair_boarding = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'stops'


class Transfers(models.Model):
    from_stop = models.ForeignKey(Stops, models.DO_NOTHING, related_name = 'transfers_from_stop')
    to_stop = models.ForeignKey(Stops, models.DO_NOTHING, related_name = 'transfers_to_stop')
    transfer_type = models.IntegerField()
    min_transfer_time = models.IntegerField(blank=True, null=True)
    transfer_id = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'transfers'


class Translations(models.Model):
    table_name = models.TextField()
    field_name = models.TextField()
    language = models.TextField()
    record_id = models.TextField(blank=True, null=True)
    record_sub_id = models.TextField(blank=True, null=True)
    field_value = models.TextField(blank=True, null=True)
    translations_id = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'translations'


class Trips(models.Model):
    route = models.ForeignKey(Routes, models.DO_NOTHING)
    service_id = models.TextField()
    trip_id = models.TextField(primary_key=True)
    trip_headsign = models.TextField(blank=True, null=True)
    direction_id = models.BooleanField(blank=True, null=True)
    block_id = models.TextField(blank=True, null=True)
    shape_id = models.TextField(blank=True, null=True)
    trip_short_name = models.TextField(blank=True, null=True)
    wheelchair_accessible = models.IntegerField(blank=True, null=True)
    bikes_allowed = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trips'


class ValidateFeedback(models.Model):
    validate_feedback_id = models.AutoField(primary_key=True)
    feedback = models.ForeignKey(Feedback, models.DO_NOTHING, blank=True, null=True)
    facility_id = models.TextField(blank=True, null=True)
    user = models.ForeignKey(Client, models.DO_NOTHING, blank=True, null=True)
    is_true = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'validate_feedback'
        unique_together = (('user', 'feedback'),)
