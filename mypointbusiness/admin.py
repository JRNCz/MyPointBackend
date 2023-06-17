import csv
from datetime import  datetime
import os
import random
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path 
from django import forms
import pandas as pd 
from .models import *
import mypointbusiness.models as models

class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()
    
def export_to_csv(modeladmin, request, queryset, fields, filename):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    writer = csv.writer(response)
    writer.writerow(fields)
    
    data = queryset.values_list(*fields)
    
    for row in data:
        writer.writerow(row)
    
    return response

# Register your models here.


class AgencyAdmin(admin.ModelAdmin):
    list_display = ('agency_id', 'agency_name', 'agency_url', 'agency_timezone', 'agency_lang', 'agency_phone', 'agency_fare_url', 'agency_email')

    def export_agencyCSV(self, request, queryset):
        fields = ['agency_id', 'agency_name', 'agency_url', 'agency_timezone', 'agency_lang', 'agency_phone', 'agency_fare_url', 'agency_email']
        filename = 'agency.csv'
        return export_to_csv(self, request, queryset, fields, filename)
    
    def get_urls5(self):
        urls = super().get_urls()
        my_urls = [path("upload-csv/", self.upload_csv)]
        return my_urls + urls

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path("delete-gtfs/", self.delete_gtfs)]
        return my_urls + urls
    
    def upload_csv(self,request):
        if request.method == 'POST':
            print('the request is a post')
            try:
                csv_file = request.FILES['csv_upload']

                normalizeGTFS(csv_file)
                return HttpResponse("CSV file uploaded successfully!")
            except Exception as e:
                print(f"An error occurred: {e}")
                return HttpResponse("Error")

                

                                               
            # file_data = csv_file.read().decode("utf-8")
            # # split by line
            # csv_data = file_data.split("\n")
            # # for each line spilleted by , 
            # for x in csv_data:
            #     fields = x.split(",")
            #     print(fields[0])
            #     print(fields[1])
                
        if request.method == 'GET':
           
            formagency = CsvImportForm()
            formstops = CsvImportForm()
            formcalendar_dates = CsvImportForm()
            formcalendar = CsvImportForm()
            formroutes = CsvImportForm()
            formtrips = CsvImportForm()
            formshapes = CsvImportForm()
            formstops = CsvImportForm()
            formstop_times = CsvImportForm()
            formfrequencies= CsvImportForm()
            formfeed_info = CsvImportForm()
            formfare_atributtes = CsvImportForm()
            form_bus = CsvImportForm()

            data ={
                "formagency": formagency,
                "formstops": formstops,
                "formcalendar_dates": formcalendar_dates,
                "formcalendar": formcalendar,
                "formroutes": formroutes,
                "formtrips": formtrips,
                "formshapes": formshapes,
                "formstop_times": formstop_times,
                "formfrequencies": formfrequencies,
                "formfeed_info": formfeed_info,
                "formfare_atributtes": formfare_atributtes,
                "form_bus": form_bus
            }
            return render(request, "admin/uploadfile.html",data)
    
    def delete_gtfs(self,request):
        
            if request.method == 'POST':
                print('a')
                    
            if request.method == 'GET':

                return render(request, "admin/deletefiles.html")
        
    export_agencyCSV.short_description = 'Export to CSV'
    actions = [export_agencyCSV]

class ClientAdmin(admin.ModelAdmin):
    list_display = ('username', 'points', 'password', 'last_login', 'id', 'email', 'reputation', 'level')
    
    def export_clientsCSV(self, request, queryset):
        fields = ['username', 'points', 'password', 'last_login', 'id', 'email', 'reputation', 'level']
        filename = 'clients.csv'
        return export_to_csv(self, request, queryset, fields, filename)
    
    export_clientsCSV.short_description = 'Export to CSV'
    actions = [export_clientsCSV]


def export_to_csv(modeladmin, request, queryset, fields, filename):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    writer = csv.writer(response)
    writer.writerow(fields)
    
    data = queryset.values_list(*fields)
    
    for row in data:
        writer.writerow(row)
    
    return response

# Register your models here.

class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop_id')
    
    def export_shopCSV(self, request, queryset):
        fields = ['name', 'shop_id']
        filename = 'shops.csv'
        return export_to_csv(self, request, queryset, fields, filename)
    
    export_shopCSV.short_description = 'Export to CSV'
    actions = [export_shopCSV]


class FeedbackcatAdmin(admin.ModelAdmin): 
    list_display = ('feedback_category', 'feedback_category_short', 'color_red', 'color_blue', 'color_green', 'imageurl')
    
    def export_feedbackcatCSV(self, request, queryset):
        fields = ['feedback_category', 'feedback_category_short', 'color_red', 'color_blue', 'color_green', 'imageurl']
        filename = 'feedback_categories.csv'
        return export_to_csv(self, request, queryset, fields, filename)
    
    export_feedbackcatCSV.short_description = 'Export to CSV'
    actions = [export_feedbackcatCSV]


class FeedbackstructAdmin(admin.ModelAdmin): 
    list_display = ('feedback_struct_id', 'facility_type', 'feedback_category', 'feedback_subcategory')
    
    def export_feedbackstructCSV(self, request, queryset):
        fields = ['feedback_struct_id', 'facility_type', 'feedback_category', 'feedback_subcategory']
        filename = 'feedback_structs.csv'
        return export_to_csv(self, request, queryset, fields, filename)
    
    export_feedbackstructCSV.short_description = 'Export to CSV'
    actions = [export_feedbackstructCSV]


class FeedbacksubcatAdmin(admin.ModelAdmin):
    list_display = ('feedback_subcategory', 'feedback_subcategory_short', 'color_red', 'color_blue', 'color_green', 'imageurl')
    
    def export_feedbacksubcatCSV(self, request, queryset):
        fields = ['feedback_subcategory', 'feedback_subcategory_short', 'color_red', 'color_blue', 'color_green', 'imageurl']
        filename = 'feedback_subcategories.csv'
        return export_to_csv(self, request, queryset, fields, filename)
    
    export_feedbacksubcatCSV.short_description = 'Export to CSV'
    actions = [export_feedbacksubcatCSV]

class BusAdmin(admin.ModelAdmin):
    list_display = ('facility', 'unit_number', 'registration_plate', 'bus_desc', 'capacity', 'standing_capacity', 'seats')

    def export_busCSV(self, request, queryset):
        fields = ['facility', 'unit_number', 'registration_plate', 'bus_desc', 'capacity', 'standing_capacity', 'seats']
        filename = 'buses.csv'
        return export_to_csv(self, request, queryset, fields, filename)

    export_busCSV.short_description = 'Export to CSV'
    actions = [export_busCSV]


class CalendarAdmin(admin.ModelAdmin):
    list_display = ('service_id', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'start_date', 'end_date')

    def export_calendarCSV(self, request, queryset):
        fields = ['service_id', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'start_date', 'end_date']
        filename = 'calendars.csv'
        return export_to_csv(self, request, queryset, fields, filename)

    export_calendarCSV.short_description = 'Export to CSV'
    actions = [export_calendarCSV]


class CalendarDatesAdmin(admin.ModelAdmin):
    list_display = ('service_id', 'date', 'exception_type', 'calendar_dates_id')

    def export_calendar_datesCSV(self, request, queryset):
        fields = ['service_id', 'date', 'exception_type', 'calendar_dates_id']
        filename = 'calendar_dates.csv'
        return export_to_csv(self, request, queryset, fields, filename)

    export_calendar_datesCSV.short_description = 'Export to CSV'
    actions = [export_calendar_datesCSV]


class CarparkAdmin(admin.ModelAdmin):
    list_display = ('name', 'facility', 'park_lat', 'park_lon', 'parking_time')

    def export_carparkCSV(self, request, queryset):
        fields = ['name', 'facility', 'park_lat', 'park_lon', 'parking_time']
        filename = 'carparks.csv'
        return export_to_csv(self, request, queryset, fields, filename)

    export_carparkCSV.short_description = 'Export to CSV'
    actions = [export_carparkCSV]


class FacilityAdmin(admin.ModelAdmin):
    list_display = ('facility_id',)

    def export_facilityCSV(self, request, queryset):
        fields = ['facility_id']
        filename = 'facilities.csv'
        return export_to_csv(self, request, queryset, fields, filename)

    export_facilityCSV.short_description = 'Export to CSV'
    actions = [export_facilityCSV]


class FacilityTypeAdmin(admin.ModelAdmin):
    list_display = ('facility_type_id', 'facility_type_name')

    def export_facility_typeCSV(self, request, queryset):
        fields = ['facility_type_id', 'facility_type_name']
        filename = 'facility_types.csv'
        return export_to_csv(self, request, queryset, fields, filename)

    export_facility_typeCSV.short_description = 'Export to CSV'
    actions = [export_facility_typeCSV]


class FareAttributesAdmin(admin.ModelAdmin):
    list_display = ('fare_id', 'price', 'currency_type', 'payment_method', 'transfers', 'transfer_duration')

    def export_fare_attributesCSV(self, request, queryset):
        fields = ['fare_id', 'price', 'currency_type', 'payment_method', 'transfers', 'transfer_duration']
        filename = 'fare_attributes.csv'
        return export_to_csv(self, request, queryset, fields, filename)

    export_fare_attributesCSV.short_description = 'Export to CSV'
    actions = [export_fare_attributesCSV]


class FareRulesAdmin(admin.ModelAdmin):
    list_display = ('fare', 'route', 'origin_id', 'destination_id', 'contains_id')

    def export_fare_rulesCSV(self, request, queryset):
        fields = ['fare', 'route', 'origin_id', 'destination_id', 'contains_id']
        filename = 'fare_rules.csv'
        return export_to_csv(self, request, queryset, fields, filename)

    export_fare_rulesCSV.short_description = 'Export to CSV'
    actions = [export_fare_rulesCSV]


class FeedInfoAdmin(admin.ModelAdmin):
    list_display = ('feed_publisher_name', 'feed_publisher_url', 'feed_lang', 'feed_start_date', 'feed_end_date', 'feed_version', 'feed_contact_email', 'feed_contact_url')

    def export_feed_infoCSV(self, request, queryset):
        fields = ['feed_publisher_name', 'feed_publisher_url', 'feed_lang', 'feed_start_date', 'feed_end_date', 'feed_version', 'feed_contact_email', 'feed_contact_url']
        filename = 'feed_info.csv'
        return export_to_csv(self, request, queryset, fields, filename)

    export_feed_infoCSV.short_description = 'Export to CSV'
    actions = [export_feed_infoCSV]


class FeedbackcatAdmin(admin.ModelAdmin):
    list_display = ('feedback_category', 'feedback_category_short', 'color_red', 'color_blue', 'color_green', 'imageurl')

    def export_feedbackcatCSV(self, request, queryset):
        fields = ['feedback_category', 'feedback_category_short', 'color_red', 'color_blue', 'color_green', 'imageurl']
        filename = 'feedback_categories.csv'
        return export_to_csv(self, request, queryset, fields, filename)

    export_feedbackcatCSV.short_description = 'Export to CSV'
    actions = [export_feedbackcatCSV]
class FeedbackstructAdmin(admin.ModelAdmin):
    list_display = ('feedback_struct_id', 'facility_type', 'feedback_category', 'feedback_subcategory')

    def export_feedbackstructCSV(self, request, queryset):
        fields = ['feedback_struct_id', 'facility_type', 'feedback_category', 'feedback_subcategory']
        filename = 'feedback_structs.csv'
        return export_to_csv(self, request, queryset, fields, filename)

    export_feedbackstructCSV.short_description = 'Export to CSV'
    actions = [export_feedbackstructCSV]


class FeedbacksubcatAdmin(admin.ModelAdmin):
    list_display = ('feedback_subcategory', 'feedback_subcategory_short', 'color_red', 'color_blue', 'color_green', 'imageurl')

    def export_feedbacksubcatCSV(self, request, queryset):
        fields = ['feedback_subcategory', 'feedback_subcategory_short', 'color_red', 'color_blue', 'color_green', 'imageurl']
        filename = 'feedback_subcategories.csv'
        return export_to_csv(self, request, queryset, fields, filename)

    export_feedbacksubcatCSV.short_description = 'Export to CSV'
    actions = [export_feedbacksubcatCSV]


class FrequenciesAdmin(admin.ModelAdmin):
    list_display = ('trip', 'start_time', 'end_time', 'headway_secs', 'exact_times', 'frequency_id')

    def export_frequenciesCSV(self, request, queryset):
        fields = ['trip', 'start_time', 'end_time', 'headway_secs', 'exact_times', 'frequency_id']
        filename = 'frequencies.csv'
        return export_to_csv(self, request, queryset, fields, filename)

    export_frequenciesCSV.short_description = 'Export to CSV'
    actions = [export_frequenciesCSV]


class GiveFeedbackAdmin(admin.ModelAdmin):
    list_display = ('give_feedback_id', 'feedback', 'facility_id', 'user')

    def export_give_feedbackCSV(self, request, queryset):
        fields = ['give_feedback_id', 'feedback', 'facility_id', 'user']
        filename = 'give_feedbacks.csv'
        return export_to_csv(self, request, queryset, fields, filename)

    export_give_feedbackCSV.short_description = 'Export to CSV'
    actions = [export_give_feedbackCSV]


class HasFacilitiesAdmin(admin.ModelAdmin):
    list_display = ('has_facilities_id', 'facility_type', 'facility')

    def export_has_facilitiesCSV(self, request, queryset):
        fields = ['has_facilities_id', 'facility_type', 'facility']
        filename = 'has_facilities.csv'
        return export_to_csv(self, request, queryset, fields, filename)

    export_has_facilitiesCSV.short_description = 'Export to CSV'
    actions = [export_has_facilitiesCSV]


class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'category', 'name', 'price', 'shop', 'quantity')

    def export_itemCSV(self, request, queryset):
        fields = ['item_id', 'category', 'name', 'price', 'shop', 'quantity']
        filename = 'items.csv'
        return export_to_csv(self, request, queryset, fields, filename)

    export_itemCSV.short_description = 'Export to CSV'
    actions = [export_itemCSV]


class LevelsAdmin(admin.ModelAdmin):
    list_display = ('level_id', 'level_index', 'level_name')

    def export_levelsCSV(self, request, queryset):
        fields = ['level_id', 'level_index', 'level_name']
        filename = 'levels.csv'
        return export_to_csv(self, request, queryset, fields, filename)

    export_levelsCSV.short_description = 'Export to CSV'
    actions = [export_levelsCSV]


class MobilityStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'facility', 'mobility_lat', 'mobility_lon')

    def export_mobility_stationCSV(self, request, queryset):
        fields = ['name', 'facility', 'mobility_lat', 'mobility_lon']
        filename = 'mobility_stations.csv'
        return export_to_csv(self, request, queryset, fields, filename)

    export_mobility_stationCSV.short_description = 'Export to CSV'
    actions = [export_mobility_stationCSV]


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('orders_id', 'item', 'user', 'quantity', 'order_date')

    def export_ordersCSV(self, request, queryset):
        fields = ['orders_id', 'item', 'user', 'quantity', 'order_date']
        filename = 'orders.csv'
        return export_to_csv(self, request, queryset, fields, filename)

    export_ordersCSV.short_description = 'Export to CSV'
    actions = [export_ordersCSV]


class PathwaysAdmin(admin.ModelAdmin):
    list_display = ('pathway_id', 'from_stop', 'to_stop', 'pathway_mode', 'is_bidirectional', 'length', 'traversal_time', 'stair_count', 'max_slope', 'min_width', 'signposted_as', 'reversed_signposted_as')

    def export_pathwaysCSV(self, request, queryset):
        fields = ['pathway_id', 'from_stop', 'to_stop', 'pathway_mode', 'is_bidirectional', 'length', 'traversal_time', 'stair_count', 'max_slope', 'min_width', 'signposted_as', 'reversed_signposted_as']
        filename = 'pathways.csv'
        return export_to_csv(self, request, queryset, fields, filename)

    export_pathwaysCSV.short_description = 'Export to CSV'
    actions = [export_pathwaysCSV]

class RailAdmin(admin.ModelAdmin):
    list_display = ('route', 'facility', 'agency_id')

    def export_railCSV(self, request, queryset):
        fields = ['route', 'facility', 'agency_id']
        filename = 'rails.csv'
        return export_to_csv(self, request, queryset, fields, filename)

    export_railCSV.short_description = 'Export to CSV'
    actions = [export_railCSV]


class RoutesAdmin(admin.ModelAdmin):
    list_display = ('route_id', 'agency', 'route_short_name', 'route_long_name', 'route_desc', 'route_type', 'route_url', 'route_color', 'route_text_color')

    def export_routesCSV(self, request, queryset):
        fields = ['route_id', 'agency', 'route_short_name', 'route_long_name', 'route_desc', 'route_type', 'route_url', 'route_color', 'route_text_color']
        filename = 'routes.csv'
        return export_to_csv(self, request, queryset, fields, filename)

    export_routesCSV.short_description = 'Export to CSV'
    actions = [export_routesCSV]


class ShapesAdmin(admin.ModelAdmin):
    list_display = ('shpid', 'shape_id', 'shape_pt_lat', 'shape_pt_lon', 'shape_pt_sequence', 'shape_dist_traveled')

    def export_shapesCSV(self, request, queryset):
        fields = ['shpid', 'shape_id', 'shape_pt_lat', 'shape_pt_lon', 'shape_pt_sequence', 'shape_dist_traveled']
        filename = 'shapes.csv'
        return export_to_csv(self, request, queryset, fields, filename)

    export_shapesCSV.short_description = 'Export to CSV'
    actions = [export_shapesCSV]


class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop_id')

    def export_shopCSV(self, request, queryset):
        fields = ['name', 'shop_id']
        filename = 'shops.csv'
        return export_to_csv(self, request, queryset, fields, filename)

    export_shopCSV.short_description = 'Export to CSV'
    actions = [export_shopCSV]


class StopTimesAdmin(admin.ModelAdmin):
    list_display = ('trip', 'arrival_time', 'departure_time', 'stop', 'stop_sequence', 'stop_headsign', 'pickup_type', 'drop_off_type', 'shape_dist_traveled', 'timepoint', 'stop_times_id')

    def export_stop_timesCSV(self, request, queryset):
        fields = ['trip', 'arrival_time', 'departure_time', 'stop', 'stop_sequence', 'stop_headsign', 'pickup_type', 'drop_off_type', 'shape_dist_traveled', 'timepoint', 'stop_times_id']
        filename = 'stop_times.csv'
        return export_to_csv(self, request, queryset, fields, filename)

    export_stop_timesCSV.short_description = 'Export to CSV'
    actions = [export_stop_timesCSV]


class StopsAdmin(admin.ModelAdmin):
    list_display = ('stop', 'stop_code', 'stop_name', 'stop_desc', 'stop_lat', 'stop_lon', 'zone_id', 'stop_url', 'location_type', 'parent_station', 'stop_timezone', 'wheelchair_boarding')

    def export_stopsCSV(self, request, queryset):
        fields = ['stop', 'stop_code', 'stop_name', 'stop_desc', 'stop_lat', 'stop_lon', 'zone_id', 'stop_url', 'location_type', 'parent_station', 'stop_timezone', 'wheelchair_boarding']
        filename = 'stops.csv'
        return export_to_csv(self, request, queryset, fields, filename)

    export_stopsCSV.short_description = 'Export to CSV'
    actions = [export_stopsCSV]


class TransfersAdmin(admin.ModelAdmin):
    list_display = ('from_stop', 'to_stop', 'transfer_type', 'min_transfer_time', 'transfer_id')

    def export_transfersCSV(self, request, queryset):
        fields = ['from_stop', 'to_stop', 'transfer_type', 'min_transfer_time', 'transfer_id']
        filename = 'transfers.csv'
        return export_to_csv(self, request, queryset, fields, filename)

    export_transfersCSV.short_description = 'Export to CSV'
    actions = [export_transfersCSV]


class TranslationsAdmin(admin.ModelAdmin):
    list_display = ('table_name', 'field_name', 'language', 'record_id', 'record_sub_id', 'field_value', 'translations_id')

    def export_translationsCSV(self, request, queryset):
        fields = ['table_name', 'field_name', 'language', 'record_id', 'record_sub_id', 'field_value', 'translations_id']
        filename = 'translations.csv'
        return export_to_csv(self, request, queryset, fields, filename)

    export_translationsCSV.short_description = 'Export to CSV'
    actions = [export_translationsCSV]


class TripsAdmin(admin.ModelAdmin):
    list_display = ('route', 'service_id', 'trip_id', 'trip_headsign', 'direction_id', 'block_id', 'shape_id', 'trip_short_name', 'wheelchair_accessible', 'bikes_allowed')

    def export_tripsCSV(self, request, queryset):
        fields = ['route', 'service_id', 'trip_id', 'trip_headsign', 'direction_id', 'block_id', 'shape_id', 'trip_short_name', 'wheelchair_accessible', 'bikes_allowed']
        filename = 'trips.csv'
        return export_to_csv(self, request, queryset, fields, filename)

    export_tripsCSV.short_description = 'Export to CSV'
    actions = [export_tripsCSV]


class ValidateFeedbackAdmin(admin.ModelAdmin):
    list_display = ('validate_feedback_id', 'feedback', 'facility_id', 'user', 'is_true')

    def export_validate_feedbackCSV(self, request, queryset):
        fields = ['validate_feedback_id', 'feedback', 'facility_id', 'user', 'is_true']
        filename = 'validate_feedback.csv'
        return export_to_csv(self, request, queryset, fields, filename)

    export_validate_feedbackCSV.short_description = 'Export to CSV'
    actions = [export_validate_feedbackCSV]


admin.site.site_header  =  "MyPoint Admin webpage"  
admin.site.site_title  =  "MyPoint admin"
admin.site.index_title  =  "Welcome to myPoint's control center!"
admin.site.register(Client, ClientAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Feedbackcat, FeedbackcatAdmin)
admin.site.register(Feedbackstruct, FeedbackstructAdmin)
admin.site.register(Feedbacksubcat, FeedbacksubcatAdmin)
admin.site.register(Agency, AgencyAdmin)
admin.site.register(Bus, BusAdmin)
admin.site.register(Calendar, CalendarAdmin)
admin.site.register(CalendarDates, CalendarDatesAdmin)
admin.site.register(Carpark, CarparkAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(Facilitytype, FacilityTypeAdmin)
admin.site.register(FareAttributes, FareAttributesAdmin)
admin.site.register(FareRules, FareRulesAdmin)
admin.site.register(FeedInfo, FeedInfoAdmin)
admin.site.register(Frequencies, FrequenciesAdmin)
admin.site.register(GiveFeedback, GiveFeedbackAdmin)
admin.site.register(HasFacilities, HasFacilitiesAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Levels, LevelsAdmin)
admin.site.register(Mobilitystation, MobilityStationAdmin)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(Pathways, PathwaysAdmin)
admin.site.register(Rail, RailAdmin)
admin.site.register(Routes, RoutesAdmin)
admin.site.register(Shapes, ShapesAdmin)
admin.site.register(StopTimes, StopTimesAdmin)
admin.site.register(Stops, StopsAdmin)
admin.site.register(Transfers, TransfersAdmin)
admin.site.register(Translations, TranslationsAdmin)
admin.site.register(Trips, TripsAdmin)
admin.site.register(ValidateFeedback, ValidateFeedbackAdmin)


agency_attributes = ["agency_id", "agency_name", "agency_url", "agency_timezone", "agency_lang", "agency_phone", "agency_fare_url", "agency_email"]
stops_attributes = ["stop_id", "stop_code", "stop_name", "stop_desc", "stop_lat", "stop_lon", "zone_id", "stop_url", "location_type", "parent_station", "stop_timezone", "wheelchair_boarding"]
routes_attributes = ["route_id", "agency_id", "route_short_name", "route_long_name", "route_desc", "route_type", "route_url", "route_color", "route_text_color"]
trips_attributes = ["route_id", "service_id", "trip_id", "trip_headsign", "direction_id", "block_id", "shape_id", "trip_short_name", "wheelchair_accessible", "bikes_allowed"]
stop_times_attributes = ["trip_id", "arrival_time", "departure_time", "stop_id", "stop_sequence", "stop_headsign", "pickup_type", "drop_off_type", "shape_dist_traveled", "timepoint"]
calendar_attributes = ["service_id", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "start_date", "end_date"]
calendar_dates_attributes = ["service_id", "date", "exception_type"]
fare_attributes_attributes = ["fare_id", "price", "currency_type", "payment_method", "transfers", "transfer_duration"]
fare_rules_attributes = ["fare_id", "route_id", "origin_id", "destination_id", "contains_id"]
shapes_attributes = ["shape_id", "shape_pt_lat", "shape_pt_locsn", "shape_pt_sequence", "shape_dist_traveled"]
frequencies_attributes = ['trip_id','start_time','end_time','headway_secs','exact_times']
transfers_attributes = ['from_stop_id','to_stop_id','transfer_type','min_transfer_time']
pathways_attributes = ['pathway_id','from_stop_id','to_stop_id','pathway_mode','is_bidirectional','length','traversal_time','stair_count','max_slope','min_width','signposted_as','reversed_signposted_as']
levels_attributes = ['level_id','level_index','level_name']
feed_info_attributes = ['feed_publisher_name','feed_publisher_url','feed_lang','feed_start_date','feed_end_date','feed_version','feed_contact_email','feed_contact_url']
translations_attributes = ['table_name','field_name','language','record_id','record_sub_id','field_value']


# FUNCTIONS
# used to normalize the Data

# Find if there's a matching column name in attributes array
def findColumn(column,attributes):
    try:
        for attribute in attributes: 
            if (column == attribute):
                return True 
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
    

# Remove columns that are not on par with the data model
def RemoveColumns(list_of_column_names,data,attributes):
    try:
        for column in list_of_column_names: 
            found = findColumn(column,attributes)
            if(found == False):
                data.drop(column, inplace=True, axis=1)  
        return data
    except Exception as e:
        print(f"An error occurred: {e}")


#Add columns that are on par with the data model and are not within the data set 
def AddColumns(list_of_column_names,data,attributes):
    try:
        for column in attributes: 
            found = findColumn(column,list_of_column_names)
            if (found == False):
                data[column]=''
        return data
    except Exception as e:
        print(f"An error occurred: {e}")

def generate_random_id(length):
    carpark = "carpark"
    digits = "0123456789"
    for _ in range(length):
        carpark += random.choice(digits)
    return carpark        

# Normalizes a File. Removes columns that are not within the data model + Adds columns that should be in the dataset with empty values
def normalizeFile(file,attributes,Table):
    try:
    # Read a file in CSV format ; Assumes that all values are string so it wont change integers to floats, dates ect...
        data = pd.read_csv(file) 
        list_of_column_names = list(data.columns)
        #print(list_of_column_names)           
        # Take the columns that are not in the model
        data=RemoveColumns(list_of_column_names,data,attributes)
        # Add columns that are on the data model but are not on the dataset
        data=AddColumns(list_of_column_names,data,attributes)
        #print('\n Final Result : \n')
        #print(data)
        data = data.reindex(columns=attributes)
        print(data)
        current_directory = os.path.dirname(os.path.abspath(__file__))
        
        now =datetime.now()
        date_time = now.strftime("%m-%d-%Y_%H-%M-%S")
        print(date_time)
        print(current_directory)
        print(Table._meta.model_name)
        print(type(current_directory))
        print(type(Table._meta.model_name))
        filename = Table._meta.model_name+date_time

        csvfile = data.to_csv("temporaryfiles/normalizedInputs/"+filename,index=False)

        insert_count = Table.objects.from_csv("temporaryfiles/normalizedInputs/example.csv")
        print("{} records inserted".format(insert_count))


    except Exception as e:
        print(f"An error occurred NormalizeFile: {e}")
    

def normalizeGTFS(file):
    filename = str(file)
    try:
        if filename == 'agency.txt':
            attributes = agency_attributes
            table=Agency
        elif filename == 'stops.txt':
            attributes = stops_attributes
            table=Stops
        elif filename == 'routes.txt':
            attributes = routes_attributes
            table= Routes
        elif filename == 'trips.txt':
            attributes = trips_attributes
            table= Trips
        elif filename == 'stop_times.txt':
            attributes = stop_times_attributes
            table= StopTimes
        elif filename == 'calendar.txt':
            attributes = calendar_attributes
            table= Calendar
        elif filename == 'calendar_dates.txt':
            attributes = calendar_dates_attributes
            table= CalendarDates
        elif filename == 'fare_attributes.txt':
            attributes = fare_attributes_attributes
            table= FareAttributes
        elif filename == 'fare_rules.txt':
            attributes = fare_rules_attributes
            table= FareRules
        elif filename == 'shapes.txt':
            attributes = shapes_attributes
            table= Shapes
        elif filename == 'frequencies.txt':
            attributes = frequencies_attributes
            table= Frequencies
        elif filename == 'transfers.txt':
            attributes = transfers_attributes
            table= Transfers
        elif filename == 'pathways.txt':
            attributes = pathways_attributes
            table= Pathways
        elif filename == 'levels.txt':
            attributes = levels_attributes
            table= Levels
        elif filename == 'feed_info.txt':
            table= FeedInfo
            attributes = feed_info_attributes
        elif filename == 'translations.txt':
            attributes = translations_attributes
            table= Translations

        else:
            print('Invalid filename->', filename)
            return

        normalizeFile(file,attributes,table)
    except Exception as e:
        print(f"An error occurred: {e}")
