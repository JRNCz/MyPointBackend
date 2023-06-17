
import datetime
import random
import string
import traceback
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.views import Response 
from rest_framework import status
from mypointapi.serializer import FeedbackstructSerializer
from mypointapi.serializer import CategoriesInfoSerializer
from mypointapi.serializer import FeedbackcatSerializer
from mypointapi.serializer import FeedbacksubcatSerializer
from mypointapi.serializer import CarParkSerializer
from mypointapi.serializer import CarParkFeedbackSerializer
from mypointapi.serializer import AccoutgetPointsSerializer
from mypointapi.serializer import OrderSerializer
from mypointbusiness.models import Orders
from mypointbusiness.models import Carpark
from mypointbusiness.models import Feedbacksubcat
from mypointbusiness.models import Feedbackcat
from mypointbusiness.models import Feedbackstruct
from mypointbusiness.models import Feedback
from mypointbusiness.models import Client 
from mypointbusiness.models import Facility
from mypointbusiness.models import Stops
from mypointbusiness.models import Shop 
from mypointbusiness.models import Bus 
from mypointbusiness.models import Routes
from mypointbusiness.models import Item
from mypointbusiness.models import Rail
from mypointbusiness.models import Facilitytype
from rest_framework_simplejwt.tokens import AccessToken

from mypointbusiness.models import Routes
from mypointbusiness.models import Agency
from mypointbusiness.models import Mobilitystation
from mypointbusiness.models import CalendarDates
from mypointbusiness.models import Trips
from mypointbusiness.models import HasFacilities
from mypointbusiness.models import StopTimes
from mypointbusiness.models import Calendar 
from mypointbusiness.models import Shapes
from mypointbusiness.models import ValidateFeedback
from mypointbusiness.models import GiveFeedback
from mypointapi.serializer  import AccoutInfoSerializer, ClientSerializer,RegisterSerializer, LoginSerializer,FacilitiesSerializer,FeedbackSerializer,StopsSerializer,ShopSerializer
from mypointapi.serializer  import ItemSerializer,BusSerializer,RailSerializer,FacilityTypeSerializer,AgencySerializer,RouteSerializer,CalendarDatesSerializer,TripsSerializer
from mypointapi.serializer  import StopTimesSerializer,CalendarSerializer,ShapesSerializer,FeedbackGivenSerializer,FeedbackValidationSerializer
from mypointapi.serializer import ClientSerializer
from mypointapi.serializer import RegisterSerializer
from mypointapi.serializer import StopsSerializer
from mypointapi.serializer import AccoutInfoSerializer
from mypointapi.serializer import FacilitiesSerializer
from mypointapi.serializer import HasFacilitiesSerializer
from django.utils import timezone



import json
from django.contrib.auth import authenticate, login, logout

from functools import wraps

from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
# Create your views here.


# Client GET POST DELETE UPDATE 


class AccountInfoView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request , format=None):
           usernamefromToken=request.user.username 
           client = Client.objects.get(username=usernamefromToken)
           serializer = AccoutInfoSerializer(client)
           return Response(serializer.data)
      
class ClientView(APIView):
# ALTERAR : end point perigoso meter a parte 

    def get(self, request, format = None):
        permission_classes = (IsAdminUser,)
        clients = Client.objects.all()
        serializer = ClientSerializer(clients,many = True)
        return Response(serializer.data) 
    
    def post(self, request, format = None):
        serializer = RegisterSerializer(data= request.data)
        if serializer.is_valid():
            Client.objects.create_user(request.data['username'], email=request.data['email'], 
            password=request.data['password'], first_name=request.data['first_name'] , last_name=request.data['last_name'])
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.data, status = status.HTTP_400_BAD_REQUEST)
    
    


    
class ClientDetailedView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request, pk , format=None):
            client = Client.objects.get(pk=pk)
            serializer = AccoutInfoSerializer(client)
            return Response(serializer.data)
    

    def put(self, request, pk, format = None):
        client = Client.objects.get(pk=pk)
        serializer = ClientSerializer(client,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete (self, request, pk, format = None):
        client = Client.objects.get(pk=pk)
        serializer = ClientSerializer(client,data=request.data)
        client.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
    


# Gives all the facilities that can hold transports back as bus stops, rail stations, streetcars...
class FacilityView(APIView):
    def get(self, request, format=None):
        stops = Stops.objects.all() # Queries all the stops 
        facilityjson=[]
        for stop in stops: # Check stops ids
            stop_id = stop.stop_id         
            facility_type_arr = []        
            all_entries = HasFacilities.objects.all() 
            stopNew = all_entries.filter(facility=stop_id)
            for newstops in stopNew:
                if(newstops.facility_type_id == 0):
                    facility_type_arr.append('Tram, Streetcar, Light rail station')
                if(newstops.facility_type_id == 33):
                    facility_type_arr.append('Bus stop')
                if(newstops.facility_type_id == 22):
                    facility_type_arr.append('Rail station')
        
            json_placeholder={}
            json_placeholder['stop_name']=stop.stop_name
            json_placeholder['asset_id']=stop_id
            json_placeholder['asset_type']=facility_type_arr
            json_placeholder['latitude']=stop.stop_lat
            json_placeholder['longitude']=stop.stop_lon
            facilityjson.append(json_placeholder)
        carparks = Carpark.objects.all()
        for carpark in carparks:   
            carpark_id = carpark.facility_id        
            facility_type_arr = []        
            all_entries = HasFacilities.objects.all() 
            CarParkNew = all_entries.filter(facility=carpark_id)
            for newcarpark in CarParkNew:
                if(newcarpark.facility_type_id == 8):
                    facility_type_arr.append('Car Park')
            json_placeholder={}
            json_placeholder['stop_name']='Parking'
            json_placeholder['asset_id']=carpark_id
            json_placeholder['asset_type']=facility_type_arr
            json_placeholder['latitude']=carpark.park_lat
            json_placeholder['longitude']=carpark.park_lon
            facilityjson.append(json_placeholder)
        mstations = Mobilitystation.objects.all()
        for station in mstations:   
                station_id = station.facility_id        
                facility_type_arr = []        
                all_entries = HasFacilities.objects.all() 
                stationNew = all_entries.filter(facility=station_id)
                for newstation in stationNew:
                    if(newstation.facility_type_id == 13):
                        facility_type_arr.append('Mobility Station')
                json_placeholder={}
                json_placeholder['stop_name']=station.name
                json_placeholder['asset_id']=station_id
                json_placeholder['asset_type']=facility_type_arr
                json_placeholder['latitude']=station.mobility_lat
                json_placeholder['longitude']=station.mobility_lon
                facilityjson.append(json_placeholder)
        buses = Bus.objects.all()
        for bus in buses:   
                bus_id = bus.facility_id        
                facility_type_arr = []        
                all_entries = HasFacilities.objects.all() 
                busNew = all_entries.filter(facility=bus_id)
                for newbus in busNew:
                    if(newbus.facility_type_id == 3):
                        facility_type_arr.append('Bus')
                json_placeholder={}
                json_placeholder['stop_name']=bus.bus_desc
                json_placeholder['asset_id']=bus_id
                json_placeholder['asset_type']=facility_type_arr
                facilityjson.append(json_placeholder)
            
        

        return Response(facilityjson, status=status.HTTP_200_OK)          
# ALTERAR: este endpoint tem que ter perms - isolar.   
    def post(self, request, format = None):
        serializer = FacilitiesSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.data, status = status.HTTP_400_BAD_REQUEST)
    


def CategoriesMetaData(facilityTypeId):
    try:
        result = Feedbackstruct.objects.filter(facility_type_id=facilityTypeId)
        serializer = FeedbackstructSerializer(instance= result,many = True)
        for item in serializer.data:
            category = Feedbackcat.objects.get(feedback_category = item['feedback_category'])  
            data= {
                'feedback_category_name': category.feedback_category,
                'feedback_category_imageurl' : category.imageurl,
                'feedback_category_color_red' : category.color_red,
                'feedback_category_color_green' : category.color_green,
                'feedback_category_color_blue' :  category.color_blue 
            }  
            item['feedback_category'] = data
            category = Feedbacksubcat.objects.get(feedback_subcategory = item['feedback_subcategory'])  

            data= {
                'feedback_subcategory_name': category.feedback_subcategory,
                'feedback_subcategory_imageurl' : category.imageurl,
                'feedback_subcategory_color_red' : category.color_red,
                'feedback_subcategory_color_green' : category.color_green,
                'feedback_subcategory_color_blue' :  category.color_blue 
            } 
            item['feedback_subcategory'] = data
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CategoriesView(APIView):
    def get(self, request, facilityType, format=None):
        
            if(facilityType == 'Rail'):
                result = CategoriesMetaData(2)
                return result      
            if(facilityType == 'Bus'):
                result = CategoriesMetaData(3)
                return result
            if(facilityType == 'MobilityStation'):
                result = CategoriesMetaData(13)
                return result
            if(facilityType == 'Busstop'):              
                result = CategoriesMetaData(33)
                return result
            if(facilityType == 'Railstation'):
                result = CategoriesMetaData(22)
                return result
            if(facilityType == 'SubwayMetro'):
                result = CategoriesMetaData(1)
                return result
            if(facilityType == 'TramStreetcarLightrail'):
                result = CategoriesMetaData(0)
                return result

      
class FeedbackView(APIView):
    # TO IMPLEMENT, CONFIRMATION IF THE USER IS CLOSE TO THE FACILITY
    # IN QUESTION based on coordinates of both the user and facility
    permissions_classes = ()
    authentication_classes = []
    def post(self,request, format = None ):
        serializerFeedback = FeedbackSerializer(data= request.data)
        if serializerFeedback.is_valid():
                try:
                    facilities = HasFacilities.objects.filter(facility=request.data['facility'])
                    for fac in facilities:
                        result = Feedbackstruct.objects.filter(facility_type_id=fac.facility_type)
                        serializer = FeedbackstructSerializer(instance= result,many = True)
                        for item in serializer.data:
                           if (item["feedback_category"] == request.data['feedback_category'] and item["feedback_subcategory"] == request.data['feedback_subcategory']):
                                #facility = Facility.objects.get(facility_id = request.data['facility'])
                                # Confirmar Category e Subcategory
                                serializerFeedback.save()
                                #print(facility)
                                auth_header = request.headers.get('Authorization')
                                if auth_header and auth_header.startswith('Bearer '):
                                    # Extract the token from the header
                                    access_token = auth_header.split(' ')[1]
                                    # Attempt to decode and verify the access token
                                try:
                                    token = AccessToken(access_token)
                                    # Token is valid and user is authenticated
                                    c = Client.objects.get(id=token['user_id'])
                                    c.points += 10
                                    c.save()
                                    GiveFeedback.objects.create(feedback_id = serializerFeedback.data['feedback_id'], facility_id = request.data['facility'], user_id = c.id )

                                    return Response({'points_added': '10'}, status=status.HTTP_200_OK)
                                except:
                                    return Response({'points_added': '0'}, status = status.HTTP_200_OK)
                                
                        return Response({'status' : 'facility does not have this category/'}, status = status.HTTP_400_BAD_REQUEST)
 
                except Facility.DoesNotExist :
                    return Response({'status' : 'facility does not exist'}, status = status.HTTP_400_BAD_REQUEST)
            
        else: 
            errors = serializerFeedback.errors
            return Response(errors, status = status.HTTP_400_BAD_REQUEST)

class FeedbackstructView(APIView):
    permission_classes = (IsAdminUser,)
    def get(self,request,format = None):
        struct = Feedbackstruct.objects.all()
        serializer=FeedbackstructSerializer(struct, many = True)
        return Response(serializer.data)
    
class ShopView(APIView):
    permission_classes = (IsAdminUser,)
    def get(self,request, format = None ):
        facilities = Shop.objects.all()
        serializer = ShopSerializer(facilities,many = True)
        return Response(serializer.data) 

class ItemView(APIView):
    permission_classes = (IsAdminUser,)
    def get(self,request, format = None ):
        facilities = Item.objects.all()
        serializer = ItemSerializer(facilities,many = True)
        return Response(serializer.data) 

 
            
class ItemDetailedView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request, pk, format = None ):
        try:
            item = Item.objects.get(pk=pk)
            serializerItem = ItemSerializer(item)
            shop = Shop.objects.get(pk=item.shop_id)
            serializerShop = ShopSerializer(shop)
            usernamefromToken=request.user.username 
            client = Client.objects.get(username=usernamefromToken)
            serializerClient = AccoutgetPointsSerializer(client)

            combined_data = {
            'item': serializerItem.data,
            'shop': serializerShop.data,
            'client': serializerClient.data
            }
            
            return Response(combined_data, status = status.HTTP_200_OK)
        except:
            return Response('status : error', status = status.HTTP_400_BAD_REQUEST )

    def post(self,request, pk, format = None ):
        try:
            item = Item.objects.get(pk=pk)
            if(request.user.points) >= item.price:  
                # Order table has a trigger that automatically takes quantity items from the Item table
                value = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
                order = Orders.objects.create(item=item, user=request.user,quantity=1,order_date=value)
                c=Client.objects.get(username=request.user.username)
                c.points= c.points - item.price
                c.save()
                serializer = OrderSerializer(order)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Client has no points'}, status = status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc()
            return Response({'status':'error'},status = status.HTTP_304_NOT_MODIFIED )
        



def generate_random_id(length):
    carpark = "carpark"
    digits = "0123456789"
    for _ in range(length):
        carpark += random.choice(digits)
    return carpark          
  
def create_unique_random_id(length):
    while True:
        random_id = generate_random_id(length)
        try:
           Facility.objects.get(facility_id=random_id)
        except Facility.DoesNotExist:
  
            return random_id
        
def GTFSrelatedDeleteinfo(request):
        if(request.method == 'GET'):
            def index(request):
                return render(request, "templates/admin/uploadfile.html")

class CarParkFeedbackView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request,format= None):
        serializer = CarParkFeedbackSerializer(data=request.data)
        if serializer.is_valid():
            text_id = create_unique_random_id(6)
            new_facility = Facility.objects.create(facility_id = text_id)
            new_car_park = Carpark.objects.create(name = text_id,facility=new_facility, park_lat = serializer.validated_data['user_lat'], park_lon = serializer.validated_data['user_lon'])
            new_has_facilities = HasFacilities.objects.create(facility_id = text_id,facility_type_id = 8)
            
            request.data['facility']=text_id
            serializer = FeedbackSerializer(data  = request.data)
            if serializer.is_valid():
                serializer.save()
                GiveFeedback.objects.create(feedback_id = serializer.data['feedback_id'], facility_id = text_id, user_id = request.user.id )
                c = Client.objects.get(id = request.user.id)
                c.points += 10
                c.save()

                return Response({'points_added' : '10'}, status = status.HTTP_200_OK)

class CarParkFeedbackValidateView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request,format= None):
            serializer = FeedbackSerializer(data  = request.data)
            if serializer.is_valid():
                serializer.save()
                print(serializer.data)
                ValidateFeedback.objects.create(feedback_id = serializer.data['feedback_id'], facility_id = request.data['facility'], user_id = request.user.id )
                c = Client.objects.get(id = request.user.id)
                c.points += 5 # 5 pontos por Validar um carpark
                c.save()
                
                return Response({'points_added' : '5'}, status = status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



                
class BusView(APIView):
    permission_classes = (IsAdminUser,)
    def get(self,request, format = None ):
        facilities = Bus.objects.all()
        serializer = BusSerializer(facilities,many = True)
        return Response(serializer.data) 

class RailView(APIView):
    permission_classes = (IsAdminUser,)
    def get(self,request, format = None ):
        facilities = Rail.objects.all()
        serializer = RailSerializer(facilities,many = True)
        return Response(serializer.data) 

class FacilityTypeView(APIView):
    permission_classes = (IsAdminUser,)
    def get(self,request, format = None ):
        facilities = Facilitytype.objects.all()
        serializer = FacilityTypeSerializer(facilities,many = True)
        return Response(serializer.data) 

class AgencyView(APIView):
    permission_classes = (IsAdminUser,)
    def get(self,request, format = None ):
        facilities = Agency.objects.all()
        serializer = AgencySerializer(facilities,many = True)
        return Response(serializer.data) 
    
class RouteView(APIView):
    permission_classes = (IsAdminUser,)
    def get(self,request, format = None ):
        facilities = Routes.objects.all()
        serializer = RouteSerializer(facilities,many = True)
        return Response(serializer.data)  
    
class CalendarDatesView(APIView):
    permission_classes = (IsAdminUser,)
    def get(self,request, format = None ):
        facilities = CalendarDates.objects.all()
        serializer = CalendarDatesSerializer(facilities,many = True)
        return Response(serializer.data)  

class TripView(APIView):
    permission_classes = (IsAdminUser,)
    def get(self,request, format = None ):
        facilities = Trips.objects.all()
        serializer = TripsSerializer(facilities,many = True)
        return Response(serializer.data)  

class StopTimesView(APIView):
    permission_classes = (IsAdminUser,)
    def get(self,request, format = None ):
        facilities = StopTimes.objects.all()
        serializer = StopTimesSerializer(facilities,many = True)
        return Response(serializer.data)  

class CalendarView(APIView):
    permission_classes = (IsAdminUser,)
    def get(self,request, format = None ):
        facilities = Calendar.objects.all()
        serializer = CalendarSerializer(facilities,many = True)
        return Response(serializer.data)  

class StopsView(APIView):
    permission_classes = (IsAdminUser,)
    def get(self,request, format = None ):
        facilities = Stops.objects.all()
        serializer = StopsSerializer(facilities,many = True)
        return Response(serializer.data) 

class ShapesView(APIView):
    permission_classes = (IsAdminUser,)
    def get(self,request, format = None ):
        facilities = Shapes.objects.all()
        serializer = ShapesSerializer(facilities,many = True)
        return Response(serializer.data)    

class FeedbackGivenView(APIView):
    permission_classes = (IsAdminUser,)
    def get(self,request, format = None ):
        facilities = GiveFeedback.objects.all()
        serializer = FeedbackGivenSerializer(facilities,many = True)
        return Response(serializer.data)    

class FeedbackValidationView(APIView):
    permission_classes = (IsAdminUser,)
    def get(self,request, format = None ):
        facilities = ValidateFeedback.objects.all()
        serializer = FeedbackValidationSerializer(facilities,many = True)
        return Response(serializer.data) 
          
        
            
        

        
        
        


        

    