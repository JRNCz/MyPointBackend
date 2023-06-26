from django.test import SimpleTestCase
from django.urls import reverse, resolve 

from mypointapi.views import *
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

from rest_framework.test import APITestCase #API Test cases comes with http requests
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status
from django.contrib.auth.models import User
from datetime import timedelta


from mypointbusiness.models import Client

# Endpoints testing 
# Does the URLs correspond to the views?
class ApiUrlTests(SimpleTestCase):
    
    def test_clients_url_resolves_to_client_view(self):
        url = reverse('client')
        self.assertEqual(resolve(url).func.view_class, ClientView)

    def test_detailed_client_url_resolves_to_client_detailed_view(self):
        url = reverse('detailedclient', args=[1])  # test with pk = 1
        self.assertEqual(resolve(url).func.view_class, ClientDetailedView)

    def test_token_obtain_pair_url_resolves_to_token_obtain_pair_view(self):
        url = reverse('token_obtain_pair')
        self.assertEqual(resolve(url).func.view_class, TokenObtainPairView)

    def test_token_refresh_url_resolves_to_token_refresh_view(self):
        url = reverse('token_refresh')
        self.assertEqual(resolve(url).func.view_class, TokenRefreshView)

    def test_facilities_url_resolves_to_facility_view(self):
        url = reverse('facilities')
        self.assertEqual(resolve(url).func.view_class, FacilityView)

    def test_feedback_url_resolves_to_feedback_view(self):
        url = reverse('feedback')
        self.assertEqual(resolve(url).func.view_class, FeedbackView)

    def test_stops_url_resolves_to_stops_view(self):
        url = reverse('stops')
        self.assertEqual(resolve(url).func.view_class, StopsView)

    def test_shop_url_resolves_to_shop_view(self):
        url = reverse('shop')
        self.assertEqual(resolve(url).func.view_class, ShopView)

    def test_item_url_resolves_to_item_view(self):
        url = reverse('item')
        self.assertEqual(resolve(url).func.view_class, ItemView)

    def test_bus_url_resolves_to_bus_view(self):
        url = reverse('bus')
        self.assertEqual(resolve(url).func.view_class, BusView)

    def test_rail_url_resolves_to_rail_view(self):
        url = reverse('rail')
        self.assertEqual(resolve(url).func.view_class, RailView)

    def test_facility_type_url_resolves_to_facility_type_view(self):
        url = reverse('facilitytype')
        self.assertEqual(resolve(url).func.view_class, FacilityTypeView)

    def test_facility_type_url_resolves_to_facility_type_view(self):
        url = reverse('detailedfacilitytype', args=[1])
        self.assertEqual(resolve(url).func.view_class, FacilityTypeDetailedView)


    def test_agency_url_resolves_to_agency_view(self):
        url = reverse('agency')
        self.assertEqual(resolve(url).func.view_class, AgencyView)

    def test_route_url_resolves_to_route_view(self):
        url = reverse('route')
        self.assertEqual(resolve(url).func.view_class, RouteView)

    def test_calendar_dates_url_resolves_to_calendar_dates_view(self):
        url = reverse('calendardate')
        self.assertEqual(resolve(url).func.view_class, CalendarDatesView)

    def test_trip_url_resolves_to_trip_view(self):
        url = reverse('trips')
        self.assertEqual(resolve(url).func.view_class, TripView)

    def test_stop_times_url_resolves_to_stop_times_view(self):
        url = reverse('stoptimes')
        self.assertEqual(resolve(url).func.view_class, StopTimesView)

    def test_calendar_url_resolves_to_calendar_view(self):
        url = reverse('calendar')
        self.assertEqual(resolve(url).func.view_class, CalendarView)

    def test_shapes_url_resolves_to_shapes_view(self):
        url = reverse('shapes')
        self.assertEqual(resolve(url).func.view_class, ShapesView)

    def test_feedback_given_url_resolves_to_feedback_given_view(self):
        url = reverse('feedgiven')
        self.assertEqual(resolve(url).func.view_class, FeedbackGivenView)

    def test_feedback_validation_url_resolves_to_feedback_validation_view(self):
        url = reverse('feedval')
        self.assertEqual(resolve(url).func.view_class, FeedbackValidationView)

    def test_categories_url_resolves_to_categories_view(self):
        url = reverse('category')
        self.assertEqual(resolve(url).func.view_class, CategoriesView)
        
    def test_categories_url_resolves_to_categories_view(self):
        url = reverse('categorycheck', args=['facility-type'])
        self.assertEqual(resolve(url).func.view_class, CategoriesView)

    def test_feedback_struct_url_resolves_to_feedback_struct_view(self):
        url = reverse('structfeed')
        self.assertEqual(resolve(url).func.view_class, FeedbackstructView)

    def test_item_detailed_url_resolves_to_item_detailed_view(self):
        url = reverse('itemdetailed', args=[1])  # test with pk = 1
        self.assertEqual(resolve(url).func.view_class, ItemDetailedView)

    def test_account_info_url_resolves_to_account_info_view(self):
        url = reverse('accountinfo')
        self.assertEqual(resolve(url).func.view_class, AccountInfoView)

    def test_car_park_feedback_url_resolves_to_car_park_feedback_view(self):
        url = reverse('carparkfeed')
        self.assertEqual(resolve(url).func.view_class, CarParkFeedbackView)

    def test_car_park_feedback_validate_url_resolves_to_car_park_feedback_validate_view(self):
        url = reverse('carparkvalidate')
        self.assertEqual(resolve(url).func.view_class, CarParkFeedbackValidateView)

    def test_bus_stop_info_url_resolves_to_bus_stop_info_view(self):
        url = reverse('busstop', args=['bus-stop-id'])
        self.assertEqual(resolve(url).func.view_class, BusStopInfoView)
        

# API testing 
# Does the views work as expected?
class ClientAPIViewTest(APITestCase):
    url = reverse('client')
    # endpoints are protected need to send a token
    
    def setUp(self):
        #create a user (not a client) 
        self.user = Client.objects.create_user(username='placeholder', password='password', email='joao@hotmail.com')
                # Create a JWT access token
        access_token = AccessToken.for_user(self.user)
     # Assign the JWT token to the authorization header of our client
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(access_token))
        
    
    def tearDown(self): # django does this automatically 
        pass 
    
    def test_get_clients_autheticated(self):
        # Autheticated Client can see client info
        # create a get request that requests to "clients" endpoint
        response = self.client.get(self.url)
        #confirm if the get request outputs a 200 OK 
        self.assertEqual(response.status_code , status.HTTP_403_FORBIDDEN)
        
    #Test clients requests without authorization    
    def test_get_clients_un_authenticated(self):
        #Unautheticated clients cant get other clients information
        self.client.credentials(HTTP_AUTHORIZATION='')

        response = self.client.get(self.url)  
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_post_customer_autheticated(self): 
        # Every client can create an account
        data =   {  
            "password": '232i3HJ1',
            "username": 'marcoGomes',
            "first_name": 'marco',
            "last_name": 'gomes',
            "email": 'leoremic@gmail.com',
        }
        
        response = self.client.post(self.url,data, format = 'json')
        self.assertEqual(response.data['username'],'marcoGomes')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        ##print(response.data)


        
    def test_post_customer_unautheticated(self): 
        # Every client can create an account
        self.client.credentials(HTTP_AUTHORIZATION='')


        data =   {  
            "password": '232i3HJ1',
            "username": 'marcoGomes',
            "first_name": 'marco',
            "last_name": 'gomes',
            "email": 'leoremic@gmail.com',
        }
        
        response = self.client.post(self.url,data, format = 'json')
        self.assertEqual(response.data['username'],'marcoGomes')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        ##print(response.data)


    def test_get_clients_admin(self):
        #create a user (not a client) 
        self.user = Client.objects.create_user(username='example', password='password', email='joao@hotmail.com')
        # Create a JWT access token
        self.user.is_staff=True
        self.user.save()
        access_token = AccessToken.for_user(self.user)
        # Assign the JWT token to the authorization header of our client
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(access_token))
        
        # Autheticated Client can see client info
        # create a get request that requests to "clients" endpoint
        response = self.client.get(self.url)
        #confirm if the get request outputs a 200 OK 

        self.assertEqual(response.status_code , status.HTTP_200_OK)
        ##print(response.data)


        
class ClientDetailAPIViewTest(APITestCase):
    
    url = reverse('client')
        

  
        
    def setUp(self): 
        
         #create a user (not a client) 
        self.user = Client.objects.create_user(username='placeholder', password='password', email='leoremic@gmail.com')
        #create a token 
        access_token = AccessToken.for_user(self.user)
        # Assign the JWT token to the authorization header of our client
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(access_token))
        
        data =   {  
                  
            "password": '232i3HJ1',
            "username" : "testuser",
            "first_name": 'test',
            "last_name": 'user',
            "email": 'leoremic@gmail.com',
        }
        
        
        response = self.client.post(self.url,data, format = 'json')
        self.assertEqual(response.data['username'],'testuser')

        self.id = response.data['id'] 
        
    def tearDown(self): # django does this automatically 
            pass 
                
    def test_get_DetailedClient_authenticated(self):
        #create a get request that requests to "clients" endpoint
        self.clienturl= reverse('detailedclient' , args= [self.id])

        response = self.client.get(self.clienturl)
        #confirm if the get request outputs a 200 OK 
        self.assertEqual(response.status_code , status.HTTP_403_FORBIDDEN)
        #self.assertEqual(response.data['user_id'], '302323' )

    def test_get_DetailedClient_un_authenticated(self):
        self.clienturl= reverse('detailedclient' , args= [self.id])

        self.client.force_authenticate(user = None, token = None)   
        response = self.client.get(self.clienturl)
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)  
    
    def test_delete_DetailedClient_authenticated(self):
        self.clienturl= reverse('detailedclient' , args= [self.id])
        response = self.client.delete(self.clienturl)
        self.assertEqual(response.status_code ,  status.HTTP_403_FORBIDDEN)
    
    
class AccoutInfoAPIViewTest(APITestCase):
    clienturl=reverse('accountinfo')
    
    def tearDown(self): # django does this automatically 
            pass 

    def setUp(self): 
        
         #create a user (not a client) 
        self.user = Client.objects.create_user(username='placeholder', password='password', email='leoremic@gmail.com')
        #create a token 
        access_token = AccessToken.for_user(self.user)
        # Assign the JWT token to the authorization header of our client
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(access_token))
    def tearDown(self): # django does this automatically 
            pass 
        
    def test_get_AccoutInfo_autheticated(self):
        
        response = self.client.get(self.clienturl)
        self.assertEqual(response.status_code ,  status.HTTP_200_OK)
        self.assertEqual(response.data['username'] , 'placeholder')
        ##print(response.data)
        
    def test_get_AccoutInfo_un_autheticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='')

        response = self.client.get(self.clienturl)
        self.assertEqual(response.status_code ,  status.HTTP_401_UNAUTHORIZED)
    
    def test_get_AccountInfo_admin(self):
        self.user = Client.objects.create_user(username='example', password='password', email='joao@hotmail.com')
        self.user.is_staff=True
        self.user.save()
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(access_token))
        response = self.client.get(self.clienturl)
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['username'] , 'example')


        
class FacilityViewAPIViewTest(APITestCase):
    
    clienturl = reverse('facilities')

    def tearDown(self): # django does this automatically 
            pass 

    def setUp(self): 
        
        #create a user (not a client) 
        self.user = Client.objects.create_user(username='placeholder', password='password', email='leoremic@gmail.com')
        #create a token 
        access_token = AccessToken.for_user(self.user)
        # Assign the JWT token to the authorization header of our client
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(access_token))
        
    def test_get_FacilityView_autheticated(self):
        
        response = self.client.get(self.clienturl)
        self.assertEqual(response.status_code ,  status.HTTP_200_OK)
        ##print(response.data)
        
    def test_get_FacilityView_unautheticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='')

        response = self.client.get(self.clienturl)
        self.assertEqual(response.status_code ,  status.HTTP_200_OK)
        ##print(response.data)
        
    def test_get_FacilityView_admin(self):
        self.user = Client.objects.create_user(username='example', password='password', email='joao@hotmail.com')
        self.user.is_staff=True
        self.user.save()
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(access_token))
        response = self.client.get(self.clienturl)
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        ##print(response.data)

class FacilityTypeDetailedAPIViewTest(APITestCase):
    clienturl = reverse('detailedfacilitytype', args= [2])
    def tearDown(self): # django does this automatically 
            pass 
        
    def setUp(self): 
        
        #create a user (not a client) 
        self.user = Client.objects.create_user(username='placeholder', password='password', email='leoremic@gmail.com')
        #create a token 
        access_token = AccessToken.for_user(self.user)
        # Assign the JWT token to the authorization header of our client
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(access_token))
        self.data =  {               
            "facility_type_id": 2,
            "facility_type_name": "Rail"
        }

    def test_post_facilitytypeDetailedView_autheticated(self):
        
        response = self.client.post(self.clienturl,self.data,format='json')
        self.assertEqual(response.status_code ,  status.HTTP_403_FORBIDDEN)
        
    def test_post_facilitytypeDetailedView_unautheticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='')

        response = self.client.post(self.clienturl,self.data,format='json')
        self.assertEqual(response.status_code ,  status.HTTP_401_UNAUTHORIZED)
        
    def test_post_facilitytypeDetailedView_admin(self):
        self.user = Client.objects.create_user(username='example', password='password', email='joao@hotmail.com')
        self.user.is_staff=True
        self.user.save()
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(access_token))
        response = self.client.post(self.clienturl,self.data,format='json')
        self.assertEqual(response.status_code ,  status.HTTP_200_OK)

# gets 

    def test_get_facilitytypeDetailedView_autheticated(self):
        self.user = Client.objects.create_user(username='example', password='password', email='joao@hotmail.com')
        self.user.is_staff=True
        self.user.save()
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(access_token))
        response = self.client.post(self.clienturl,self.data,format='json')
        self.assertEqual(response.status_code ,  status.HTTP_200_OK)
        
        self.user = Client.objects.create_user(username='test', password='password', email='leoremic@gmail.com')
        #create a token 
        access_token = AccessToken.for_user(self.user)
        # Assign the JWT token to the authorization header of our client
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(access_token))
        
        response = self.client.get(self.clienturl)
        self.assertEqual(response.status_code ,  status.HTTP_403_FORBIDDEN)
        
    def test_get_facilitytypeDetailedView_unautheticated(self):
        self.user = Client.objects.create_user(username='example', password='password', email='joao@hotmail.com')
        self.user.is_staff=True
        self.user.save()
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(access_token))
        response = self.client.post(self.clienturl,self.data,format='json')
        self.assertEqual(response.status_code ,  status.HTTP_200_OK)
        
        self.user = Client.objects.create_user(username='test', password='password', email='leoremic@gmail.com')
        #create a token 
        access_token = AccessToken.for_user(self.user)
        # Assign the JWT token to the authorization header of our client
        self.client.credentials(HTTP_AUTHORIZATION='')
        
        response = self.client.get(self.clienturl)
        self.assertEqual(response.status_code ,  status.HTTP_401_UNAUTHORIZED)
        
    def test_get_facilitytypeDetailedView_admin(self):
        self.user = Client.objects.create_user(username='example', password='password', email='joao@hotmail.com')
        self.user.is_staff=True
        self.user.save()
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(access_token))
        response = self.client.post(self.clienturl,self.data,format='json')
        self.assertEqual(response.status_code ,  status.HTTP_200_OK)
        response = self.client.get(self.clienturl)
        self.assertEqual(response.status_code ,  status.HTTP_200_OK)


    
class FacilityDetailedAPIViewTest(APITestCase):
    
    clienturl = reverse('detailedfacility', args= ['rail'])
    facilitytypeurl = reverse('detailedfacilitytype', args= [2])

    def tearDown(self): # django does this automatically 
            pass 
    def setUp(self): 
        
        #create a user (not a client) 
        self.user = Client.objects.create_user(username='placeholder', password='password', email='leoremic@gmail.com')
        #create a token 
        access_token = AccessToken.for_user(self.user)
        # Assign the JWT token to the authorization header of our client
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(access_token))
        self.data =  {               
        "facility": "rail1",
        "unit_number": "1-3-235",
        "registration_plate": "213239u2x-239u" ,
        "bus_desc": "",
        "capacity": 15,
        "standing_capacity": 10,
        "seats": 5
        }
        self.dataFacilityType = {               
            "facility_type_id": 2,
            "facility_type_name": "Rail"
        }

        
    def test_get_FacilityDetailedView_autheticated(self):
        
        response = self.client.post(self.clienturl,self.data,format='json')
        self.assertEqual(response.status_code ,  status.HTTP_403_FORBIDDEN)
        ##print(response.data)
        
    def test_get_FacilityDetailedView_unautheticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='')

        response = self.client.post(self.clienturl,self.data,format='json')
        self.assertEqual(response.status_code ,  status.HTTP_401_UNAUTHORIZED)
        ##print(response.data)
        
    def test_get_FacilityDetailedView_admin(self):
        
        self.user = Client.objects.create_user(username='example', password='password', email='joao@hotmail.com')
        self.user.is_staff=True
        self.user.save()
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(access_token))
        response = self.client.post(self.facilitytypeurl,self.dataFacilityType,format='json')
        self.assertEqual(response.status_code , status.HTTP_200_OK)

        response = self.client.post(self.clienturl,self.data,format='json')

        self.assertEqual(response.status_code ,  status.HTTP_200_OK)
        

class CategoriesViewAPIViewTest(APITestCase):
        clienturl = reverse('structfeed')
        facilitytypeurl = reverse('facilitytype')
        subcategoryurl = reverse('subcategory')
        categoryurl = reverse('category')
        viewcategoriesurl=reverse('categorycheck', args=['MobilityStation'])
        

        def tearDown(self): # django does this automatically 
            pass 
        def setUp(self): 

            #create a user (not a client) 
            self.user = Client.objects.create_user(username='testuser', password='password', email='joao@hotmail.com')
            self.user.is_staff=True
            self.user.save()
            access_token = AccessToken.for_user(self.user)
            # Assign the JWT token to the authorization header of our client
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(access_token))
            self.datacreateFacilityType = [
                {
                    "facility_type_id": 0,
                    "facility_type_name": "Tram, Streetcar, Light rail"
                },
                {
                    "facility_type_id": 1,
                    "facility_type_name": "Subway, Metro"
                },
                {
                    "facility_type_id": 2,
                    "facility_type_name": "Rail"
                },
                {
                    "facility_type_id": 3,
                    "facility_type_name": "Bus"
                },
                {
                    "facility_type_id": 4,
                    "facility_type_name": "Ferry"
                },
                {
                    "facility_type_id": 5,
                    "facility_type_name": "Cable tram"
                },
                {
                    "facility_type_id": 6,
                    "facility_type_name": "Aerial lift, suspended cable car"
                },
                {
                    "facility_type_id": 7,
                    "facility_type_name": "Funicular"
                },
                {
                    "facility_type_id": 8,
                    "facility_type_name": "Car Park"
                },
                {
                    "facility_type_id": 11,
                    "facility_type_name": "Trolleybus"
                },
                {
                    "facility_type_id": 12,
                    "facility_type_name": "Monorail"
                },
                {
                    "facility_type_id": 33,
                    "facility_type_name": "Bus stop"
                },
                {
                    "facility_type_id": 22,
                    "facility_type_name": "Rail station"
                },
                {
                    "facility_type_id": 13,
                    "facility_type_name": "Mobility Station"
                }
                ]
            self.datacreateFeedbackcategory = [
            {
                "feedback_category": "Quality of Service",
                "feedback_category_short": "QOS",
                "color_red": 53,
                "color_green": 182,
                "color_blue": 51,
                "imageurl": "qos.png"
            },
            {
                "feedback_category": "Security",
                "feedback_category_short": "SEC",
                "color_red": 255,
                "color_green": 0,
                "color_blue": 0,
                "imageurl": "lock.png"
            },
            {
                "feedback_category": "Maintenance",
                "feedback_category_short": "MTN",
                "color_red": 45,
                "color_green": 207,
                "color_blue": 242,
                "imageurl": "maintenance.png"
            },
            {
                "feedback_category": "General",
                "feedback_category_short": "GEN",
                "color_red": 0,
                "color_green": 0,
                "color_blue": 0,
                "imageurl": ""
            }
            ]
            self.datacreateFeedbacksubcategory = [
            {
                "feedback_subcategory": "Occupation",
                "feedback_subcategory_short": "OCP",
                "color_red": 73,
                "color_green": 169,
                "color_blue": 88,
                "imageurl": "crowd.png"
            },
            {
                "feedback_subcategory": "Costumer-service",
                "feedback_subcategory_short": "CS",
                "color_red": 69,
                "color_green": 222,
                "color_blue": 56,
                "imageurl": "support.png"
            },
            {
                "feedback_subcategory": "Cleanliness",
                "feedback_subcategory_short": "CLN",
                "color_red": 107,
                "color_green": 255,
                "color_blue": 149,
                "imageurl": "cleaning.png"
            },
            {
                "feedback_subcategory": "Comfort",
                "feedback_subcategory_short": "CMF",
                "color_red": 187,
                "color_green": 255,
                "color_blue": 202,
                "imageurl": "sofa.png"
            },
            {
                "feedback_subcategory": "Service delay",
                "feedback_subcategory_short": "SD",
                "color_red": 172,
                "color_green": 254,
                "color_blue": 195,
                "imageurl": "clock.png"
            },
            {
                "feedback_subcategory": "Personal safety",
                "feedback_subcategory_short": "PSF",
                "color_red": 178,
                "color_green": 42,
                "color_blue": 42,
                "imageurl": "protection.png"
            },
            {
                "feedback_subcategory": "Belongings safety",
                "feedback_subcategory_short": "BSF",
                "color_red": 255,
                "color_green": 77,
                "color_blue": 0,
                "imageurl": "luggage.png"
            },
            {
                "feedback_subcategory": "Lightening",
                "feedback_subcategory_short": "ILU",
                "color_red": 255,
                "color_green": 230,
                "color_blue": 0,
                "imageurl": "lamp.png"
            },
            {
                "feedback_subcategory": "Driving",
                "feedback_subcategory_short": "DRV",
                "color_red": 255,
                "color_green": 168,
                "color_blue": 0,
                "imageurl": "hands.png"
            },
            {
                "feedback_subcategory": "Infrastructure state",
                "feedback_subcategory_short": "INF",
                "color_red": 0,
                "color_green": 56,
                "color_blue": 255,
                "imageurl": "infrastructure.png"
            },
            {
                "feedback_subcategory": "Road state",
                "feedback_subcategory_short": "RoS",
                "color_red": 77,
                "color_green": 116,
                "color_blue": 255,
                "imageurl": "road.png"
            },
            {
                "feedback_subcategory": "Obstacles",
                "feedback_subcategory_short": "OBS",
                "color_red": 133,
                "color_green": 152,
                "color_blue": 255,
                "imageurl": "barrier.png"
            },
            {
                "feedback_subcategory": "Accessibility",
                "feedback_subcategory_short": "ACS",
                "color_red": 173,
                "color_green": 206,
                "color_blue": 255,
                "imageurl": "import.png"
            },
            {
                "feedback_subcategory": "Classification",
                "feedback_subcategory_short": "CLA",
                "color_red": 0,
                "color_green": 0,
                "color_blue": 0,
                "imageurl": ""
            }
            ]
            self.data=[
                {
                    "facility_type": 3,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Occupation"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Costumer-service"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Cleanliness"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Comfort"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Service delay"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Personal safety"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Belongings safety"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Lightening"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Driving"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Infrastructure state"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Road state"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Obstacles"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Accessibility"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "General",
                    "feedback_subcategory": "Classification"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Occupation"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Cleanliness"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Comfort"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Service delay"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Personal safety"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Belongings safety"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Lightening"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Driving"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Infrastructure state"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Road state"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Accessibility"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "General",
                    "feedback_subcategory": "Classification"
                },
                {
                    "facility_type": 13,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Costumer-service"
                },
                {
                    "facility_type": 13,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Cleanliness"
                },
                {
                    "facility_type": 13,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Comfort"
                },
                {
                    "facility_type": 13,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Service delay"
                },
                {
                    "facility_type": 13,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Personal safety"
                },
                {
                    "facility_type": 13,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Belongings safety"
                },
                {
                    "facility_type": 13,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Lightening"
                },
                {
                    "facility_type": 13,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Infrastructure state"
                },
                {
                    "facility_type": 13,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Accessibility"
                },
                {
                    "facility_type": 13,
                    "feedback_category": "General",
                    "feedback_subcategory": "Classification"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Occupation"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Cleanliness"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Comfort"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Service delay"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Personal safety"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Belongings safety"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Lightening"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Infrastructure state"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Road state"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Obstacles"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Accessibility"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "General",
                    "feedback_subcategory": "Classification"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Occupation"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Costumer-service"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Cleanliness"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Comfort"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Service delay"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Personal safety"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Belongings safety"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Lightening"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Infrastructure state"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Road state"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Obstacles"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Accessibility"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "General",
                    "feedback_subcategory": "Classification"
                },
                {
                    "facility_type": 8,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Occupation"
                }
                ]
        def test_get_categoriescheck(self):
            response = self.client.post(self.facilitytypeurl,self.datacreateFacilityType,format='json')
            self.assertEqual(response.status_code ,  status.HTTP_200_OK)
            #print(response.data)
            i=0
            for dic in response.data:
                #print(i)
                self.assertEqual(dic['facility_type_id'] , self.datacreateFacilityType[i]['facility_type_id'])
                self.assertEqual(dic["facility_type_name"] , self.datacreateFacilityType[i]["facility_type_name"])
                i=i+1 
            response = self.client.post(self.subcategoryurl,self.datacreateFeedbacksubcategory,format='json')
            self.assertEqual(response.status_code ,  status.HTTP_200_OK)
            i=0
            for dic in response.data:
                self.assertEqual(dic['feedback_subcategory'] , self.datacreateFeedbacksubcategory[i]['feedback_subcategory'])
                self.assertEqual(dic["feedback_subcategory_short"] , self.datacreateFeedbacksubcategory[i]["feedback_subcategory_short"])
                i=i+1
            response = self.client.post(self.categoryurl,self.datacreateFeedbackcategory,format='json')
            self.assertEqual(response.status_code ,  status.HTTP_200_OK)
            i=0
            for dic in response.data:
                self.assertEqual(dic['feedback_category'] , self.datacreateFeedbackcategory[i]['feedback_category'])
                self.assertEqual(dic["feedback_category_short"] , self.datacreateFeedbackcategory[i]["feedback_category_short"])
                i=i+1

            response = self.client.post(self.clienturl,self.data,format='json')

            self.assertEqual(response.status_code ,  status.HTTP_200_OK)
            i=0
            for dic in response.data:
                self.assertEqual(dic['facility_type'] , self.data[i]['facility_type'])
                self.assertEqual(dic["feedback_subcategory"] , self.data[i]["feedback_subcategory"])
                self.assertEqual(dic["feedback_category"] , self.data[i]["feedback_category"])
                i=i+1
                
            response = self.client.get(self.viewcategoriesurl)
            self.assertEqual(response.status_code ,  status.HTTP_200_OK)



class FeedbackAPIViewTest(APITestCase):
        carparkurl = reverse('carparkfeed')
        clienturl = reverse('structfeed')
        facilitytypeurl = reverse('facilitytype')
        subcategoryurl = reverse('subcategory')
        categoryurl = reverse('category')
        carparkvalidateurl=reverse('carparkvalidate')
        facilitystatusurl= reverse('facilities')

        def tearDown(self): # django does this automatically 
            pass 
        def setUp(self): 
            #create a user (not a client) 
            self.user = Client.objects.create_user(username='testuser', password='password', email='joao@hotmail.com')
            self.user.is_staff=True
            self.user.save()
            access_token = AccessToken.for_user(self.user)
            # Assign the JWT token to the authorization header of our client
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(access_token))
            time = timezone.now()
            one_hour_ago = time - timedelta(hours=2)

            self.carparkdata={
                "feedback_category": "Quality of Service",
                "feedback_subcategory": 'Occupation',
                "time_action": one_hour_ago,
                "score": 2,
                "image_url": None,
                "text": "Test",
                "user_lat": 10.0,
                "user_lon": 12.0,
            }
            self.datacreateFacilityType = [{
                    "facility_type_id": 0,
                    "facility_type_name": "Tram, Streetcar, Light rail"
                },
                {
                    "facility_type_id": 1,
                    "facility_type_name": "Subway, Metro"
                },
                {
                    "facility_type_id": 2,
                    "facility_type_name": "Rail"
                },
                {
                    "facility_type_id": 3,
                    "facility_type_name": "Bus"
                },
                {
                    "facility_type_id": 4,
                    "facility_type_name": "Ferry"
                },
                {
                    "facility_type_id": 5,
                    "facility_type_name": "Cable tram"
                },
                {
                    "facility_type_id": 6,
                    "facility_type_name": "Aerial lift, suspended cable car"
                },
                {
                    "facility_type_id": 7,
                    "facility_type_name": "Funicular"
                },
                {
                    "facility_type_id": 8,
                    "facility_type_name": "Car Park"
                },
                {
                    "facility_type_id": 11,
                    "facility_type_name": "Trolleybus"
                },
                {
                    "facility_type_id": 12,
                    "facility_type_name": "Monorail"
                },
                {
                    "facility_type_id": 33,
                    "facility_type_name": "Bus stop"
                },
                {
                    "facility_type_id": 22,
                    "facility_type_name": "Rail station"
                },
                {
                    "facility_type_id": 13,
                    "facility_type_name": "Mobility Station"
                }
                ]
            self.datacreateFeedbackcategory = [
            {
                "feedback_category": "Quality of Service",
                "feedback_category_short": "QOS",
                "color_red": 53,
                "color_green": 182,
                "color_blue": 51,
                "imageurl": "qos.png"
            },
            {
                "feedback_category": "Security",
                "feedback_category_short": "SEC",
                "color_red": 255,
                "color_green": 0,
                "color_blue": 0,
                "imageurl": "lock.png"
            },
            {
                "feedback_category": "Maintenance",
                "feedback_category_short": "MTN",
                "color_red": 45,
                "color_green": 207,
                "color_blue": 242,
                "imageurl": "maintenance.png"
            },
            {
                "feedback_category": "General",
                "feedback_category_short": "GEN",
                "color_red": 0,
                "color_green": 0,
                "color_blue": 0,
                "imageurl": ""
            }
            ]
            self.datacreateFeedbacksubcategory = [
            {
                "feedback_subcategory": "Occupation",
                "feedback_subcategory_short": "OCP",
                "color_red": 73,
                "color_green": 169,
                "color_blue": 88,
                "imageurl": "crowd.png"
            },
            {
                "feedback_subcategory": "Costumer-service",
                "feedback_subcategory_short": "CS",
                "color_red": 69,
                "color_green": 222,
                "color_blue": 56,
                "imageurl": "support.png"
            },
            {
                "feedback_subcategory": "Cleanliness",
                "feedback_subcategory_short": "CLN",
                "color_red": 107,
                "color_green": 255,
                "color_blue": 149,
                "imageurl": "cleaning.png"
            },
            {
                "feedback_subcategory": "Comfort",
                "feedback_subcategory_short": "CMF",
                "color_red": 187,
                "color_green": 255,
                "color_blue": 202,
                "imageurl": "sofa.png"
            },
            {
                "feedback_subcategory": "Service delay",
                "feedback_subcategory_short": "SD",
                "color_red": 172,
                "color_green": 254,
                "color_blue": 195,
                "imageurl": "clock.png"
            },
            {
                "feedback_subcategory": "Personal safety",
                "feedback_subcategory_short": "PSF",
                "color_red": 178,
                "color_green": 42,
                "color_blue": 42,
                "imageurl": "protection.png"
            },
            {
                "feedback_subcategory": "Belongings safety",
                "feedback_subcategory_short": "BSF",
                "color_red": 255,
                "color_green": 77,
                "color_blue": 0,
                "imageurl": "luggage.png"
            },
            {
                "feedback_subcategory": "Lightening",
                "feedback_subcategory_short": "ILU",
                "color_red": 255,
                "color_green": 230,
                "color_blue": 0,
                "imageurl": "lamp.png"
            },
            {
                "feedback_subcategory": "Driving",
                "feedback_subcategory_short": "DRV",
                "color_red": 255,
                "color_green": 168,
                "color_blue": 0,
                "imageurl": "hands.png"
            },
            {
                "feedback_subcategory": "Infrastructure state",
                "feedback_subcategory_short": "INF",
                "color_red": 0,
                "color_green": 56,
                "color_blue": 255,
                "imageurl": "infrastructure.png"
            },
            {
                "feedback_subcategory": "Road state",
                "feedback_subcategory_short": "RoS",
                "color_red": 77,
                "color_green": 116,
                "color_blue": 255,
                "imageurl": "road.png"
            },
            {
                "feedback_subcategory": "Obstacles",
                "feedback_subcategory_short": "OBS",
                "color_red": 133,
                "color_green": 152,
                "color_blue": 255,
                "imageurl": "barrier.png"
            },
            {
                "feedback_subcategory": "Accessibility",
                "feedback_subcategory_short": "ACS",
                "color_red": 173,
                "color_green": 206,
                "color_blue": 255,
                "imageurl": "import.png"
            },
            {
                "feedback_subcategory": "Classification",
                "feedback_subcategory_short": "CLA",
                "color_red": 0,
                "color_green": 0,
                "color_blue": 0,
                "imageurl": ""
            }
            ]
            self.data=[

                {
                    "facility_type": 3,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Occupation"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Costumer-service"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Cleanliness"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Comfort"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Service delay"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Personal safety"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Belongings safety"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Lightening"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Driving"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Infrastructure state"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Road state"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Obstacles"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Accessibility"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "General",
                    "feedback_subcategory": "Classification"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Occupation"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Cleanliness"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Comfort"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Service delay"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Personal safety"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Belongings safety"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Lightening"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Driving"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Infrastructure state"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Road state"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Accessibility"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "General",
                    "feedback_subcategory": "Classification"
                },
                {
                    "facility_type": 13,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Costumer-service"
                },
                {
                    "facility_type": 13,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Cleanliness"
                },
                {
                    "facility_type": 13,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Comfort"
                },
                {
                    "facility_type": 13,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Service delay"
                },
                {
                    "facility_type": 13,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Personal safety"
                },
                {
                    "facility_type": 13,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Belongings safety"
                },
                {
                    "facility_type": 13,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Lightening"
                },
                {
                    "facility_type": 13,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Infrastructure state"
                },
                {
                    "facility_type": 13,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Accessibility"
                },
                {
                    "facility_type": 13,
                    "feedback_category": "General",
                    "feedback_subcategory": "Classification"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Occupation"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Cleanliness"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Comfort"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Service delay"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Personal safety"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Belongings safety"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Lightening"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Infrastructure state"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Road state"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Obstacles"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Accessibility"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "General",
                    "feedback_subcategory": "Classification"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Occupation"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Costumer-service"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Cleanliness"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Comfort"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Service delay"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Personal safety"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Belongings safety"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Lightening"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Infrastructure state"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Road state"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Obstacles"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Accessibility"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "General",
                    "feedback_subcategory": "Classification"
                },
                {
                    "facility_type": 8,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Occupation"
                }
                ]
            
        def test_create_feedback(self):
            response = self.client.post(self.facilitytypeurl,self.datacreateFacilityType,format='json')
            self.assertEqual(response.status_code ,  status.HTTP_200_OK)
            #print(response.data)
            i=0
            for dic in response.data:
                #print(i)
                self.assertEqual(dic['facility_type_id'] , self.datacreateFacilityType[i]['facility_type_id'])
                self.assertEqual(dic["facility_type_name"] , self.datacreateFacilityType[i]["facility_type_name"])
                i=i+1 
            response = self.client.post(self.subcategoryurl,self.datacreateFeedbacksubcategory,format='json')
            self.assertEqual(response.status_code ,  status.HTTP_200_OK)
            i=0
            for dic in response.data:
                self.assertEqual(dic['feedback_subcategory'] , self.datacreateFeedbacksubcategory[i]['feedback_subcategory'])
                self.assertEqual(dic["feedback_subcategory_short"] , self.datacreateFeedbacksubcategory[i]["feedback_subcategory_short"])
                i=i+1
            response = self.client.post(self.categoryurl,self.datacreateFeedbackcategory,format='json')
            self.assertEqual(response.status_code ,  status.HTTP_200_OK)
            i=0
            for dic in response.data:
                self.assertEqual(dic['feedback_category'] , self.datacreateFeedbackcategory[i]['feedback_category'])
                self.assertEqual(dic["feedback_category_short"] , self.datacreateFeedbackcategory[i]["feedback_category_short"])
                i=i+1

            response = self.client.post(self.clienturl,self.data,format='json')
            #print(response.data)

            self.assertEqual(response.status_code ,  status.HTTP_200_OK)
            i=0
            for dic in response.data:
                self.assertEqual(dic['facility_type'] , self.data[i]['facility_type'])
                self.assertEqual(dic["feedback_subcategory"] , self.data[i]["feedback_subcategory"])
                self.assertEqual(dic["feedback_category"] , self.data[i]["feedback_category"])
                i=i+1
            response = self.client.post(self.carparkurl,self.carparkdata,format='json')
            self.assertEqual(response.status_code ,  status.HTTP_200_OK)
            self.assertEqual(response.data['points_added'] , '10')
            facility =  response.data['facility']     
            self.dataval={
                "feedback_category": "Quality of Service",
                "feedback_subcategory": 'Occupation',
                "time_action": timezone.now(),
                "score": 3,
                "image_url": "",
                "text": "yeee",
                "user_lat": 10.1,
                "user_lon": 12.1,
                "facility": facility
            }
            response = self.client.post(self.carparkvalidateurl,self.dataval,format='json')
            self.assertEqual(response.status_code ,  status.HTTP_200_OK)
            response = self.client.get(self.facilitystatusurl,self.dataval,format='json')
            print(response.data)
            self.assertEqual(response.status_code ,  status.HTTP_200_OK)



            
# BusStopInfoView view is a very complex endpoint to test - later
   


class ItemDetailedAPIViewTest(APITestCase):
    
        itemurl = reverse('item')
        shopurl= reverse('shop')
        buyitemurl=reverse('itemdetailed', args=[7])
        def tearDown(self): # django does this automatically 
            pass 
        
        def setUp(self): 
        
            #create a user (not a client) 
            self.user = Client.objects.create_user(username='testuser', password='password', email='joao@hotmail.com', points= 10000)
            self.user.is_staff=True
            self.user.save()
            access_token = AccessToken.for_user(self.user)
            # Assign the JWT token to the authorization header of our client
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(access_token))
            self.shopdata = [
                {
                 "name": "CAFE DO RIO"
                },
                {
                 "name": "RESTAURANTE DO ZE"
                }
                ]
            self.itemdata=[{
                "category": "BEBIDAS",
                "name": "CAFE",
                "price": 300,
                "shop": 3,
                "quantity": 20
                }]

        def test_create_item_detailed(self):
            
            response = self.client.post(self.shopurl,self.shopdata,format='json')
            self.assertEqual(response.status_code ,  status.HTTP_200_OK)
            # print(response.data)
            i=0
            for dic in response.data:
                self.assertEqual(dic['name'] , self.shopdata[i]['name'])
                i=i+1
            response = self.client.post(self.itemurl,self.itemdata,format='json')
            # print(response.data)

            self.assertEqual(response.status_code ,  status.HTTP_200_OK)
            i=0
            for dic in response.data:
                self.assertEqual(dic['name'] , self.itemdata[i]['name'])
                self.assertEqual(dic["shop"] , self.itemdata[i]['shop'])
                i=i+1
            response = self.client.post(self.buyitemurl)
            # print(response.data)
            self.assertEqual(response.status_code ,  status.HTTP_200_OK)
            


class CarParkFeedbackAPIViewTest(APITestCase):
        carparkurl = reverse('carparkfeed')
        facilitytypeurl = reverse('facilitytype')

        def tearDown(self): # django does this automatically 
            pass 
        
        def setUp(self): 
        
            #create a user (not a client) 
            self.user = Client.objects.create_user(username='testuser', password='password', email='joao@hotmail.com', points= 10000)
            self.user.is_staff=True
            self.user.save()
            access_token = AccessToken.for_user(self.user)
            # Assign the JWT token to the authorization header of our client
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(access_token))

            self.data={
                "feedback_category": "Quality of Service",
                "feedback_subcategory": 'Occupation',
                "time_action": timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                "score": 2,
                "image_url": "",
                "text": "Test",
                "user_lat": 10.0,
                "user_lon": 12.0,
            }
            self.facilitytypedata =  [  {
                    "facility_type_id": 0,
                    "facility_type_name": "Tram, Streetcar, Light rail"
                },
                {
                    "facility_type_id": 1,
                    "facility_type_name": "Subway, Metro"
                },
                {
                    "facility_type_id": 2,
                    "facility_type_name": "Rail"
                },
                {
                    "facility_type_id": 3,
                    "facility_type_name": "Bus"
                },
                {
                    "facility_type_id": 4,
                    "facility_type_name": "Ferry"
                },
                {
                    "facility_type_id": 5,
                    "facility_type_name": "Cable tram"
                },
                {
                    "facility_type_id": 6,
                    "facility_type_name": "Aerial lift, suspended cable car"
                },
                {
                    "facility_type_id": 7,
                    "facility_type_name": "Funicular"
                },
                {
                    "facility_type_id": 8,
                    "facility_type_name": "Car Park"
                },
                {
                    "facility_type_id": 11,
                    "facility_type_name": "Trolleybus"
                },
                {
                    "facility_type_id": 12,
                    "facility_type_name": "Monorail"
                },
                {
                    "facility_type_id": 33,
                    "facility_type_name": "Bus stop"
                },
                {
                    "facility_type_id": 22,
                    "facility_type_name": "Rail station"
                },
                {
                    "facility_type_id": 13,
                    "facility_type_name": "Mobility Station"
                }
                ]
                        
            

        def test_create_carpark(self):
            response = self.client.post(self.facilitytypeurl,self.facilitytypedata,format='json')
            self.assertEqual(response.status_code ,  status.HTTP_200_OK)
            i=0
            for dic in response.data:
                self.assertEqual(dic['facility_type_id'] , self.facilitytypedata[i]['facility_type_id'])
                self.assertEqual(dic["facility_type_name"] , self.facilitytypedata[i]["facility_type_name"])
                i=i+1
                
            response = self.client.post(self.carparkurl,self.data,format='json')
            self.assertEqual(response.status_code ,  status.HTTP_200_OK)
            self.assertEqual(response.data['points_added'] , '10')



class CarParkFeedbackValidateAPIViewTest(APITestCase):
        carparkurl = reverse('carparkfeed')
        facilitytypeurl = reverse('facilitytype')
        carparkvalidateurl = reverse('carparkvalidate')


        def tearDown(self): # django does this automatically 
            pass 
        
        def setUp(self): 
        
            #create a user (not a client) 
            self.user = Client.objects.create_user(username='testuser', password='password', email='joao@hotmail.com', points= 10000)
            self.user.is_staff=True
            self.user.save()
            access_token = AccessToken.for_user(self.user)
            # Assign the JWT token to the authorization header of our client
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(access_token))
            current_time = timezone.now()  # Get the current time
            one_hour_ago = current_time - timedelta(hours=1)  # Subtract one hour
            self.data={
                "feedback_category": "Quality of Service",
                "feedback_subcategory": 'Occupation',
                "time_action": timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                "score": 2,
                "image_url": "",
                "text": "Test",
                "user_lat": 10.0,
                "user_lon": 12.0,
            }
            self.facilitytypedata =  [  {
                    "facility_type_id": 0,
                    "facility_type_name": "Tram, Streetcar, Light rail"
                },
                {
                    "facility_type_id": 1,
                    "facility_type_name": "Subway, Metro"
                },
                {
                    "facility_type_id": 2,
                    "facility_type_name": "Rail"
                },
                {
                    "facility_type_id": 3,
                    "facility_type_name": "Bus"
                },
                {
                    "facility_type_id": 4,
                    "facility_type_name": "Ferry"
                },
                {
                    "facility_type_id": 5,
                    "facility_type_name": "Cable tram"
                },
                {
                    "facility_type_id": 6,
                    "facility_type_name": "Aerial lift, suspended cable car"
                },
                {
                    "facility_type_id": 7,
                    "facility_type_name": "Funicular"
                },
                {
                    "facility_type_id": 8,
                    "facility_type_name": "Car Park"
                },
                {
                    "facility_type_id": 11,
                    "facility_type_name": "Trolleybus"
                },
                {
                    "facility_type_id": 12,
                    "facility_type_name": "Monorail"
                },
                {
                    "facility_type_id": 33,
                    "facility_type_name": "Bus stop"
                },
                {
                    "facility_type_id": 22,
                    "facility_type_name": "Rail station"
                },
                {
                    "facility_type_id": 13,
                    "facility_type_name": "Mobility Station"
                }
                ]
                        
            

        def test_create_carpark_validate(self):
            response = self.client.post(self.facilitytypeurl,self.facilitytypedata,format='json')
            self.assertEqual(response.status_code ,  status.HTTP_200_OK)
            i=0
            for dic in response.data:
                self.assertEqual(dic['facility_type_id'] , self.facilitytypedata[i]['facility_type_id'])
                self.assertEqual(dic["facility_type_name"] , self.facilitytypedata[i]["facility_type_name"])
                i=i+1
                
            response = self.client.post(self.carparkurl,self.data,format='json')
            self.assertEqual(response.status_code ,  status.HTTP_200_OK)
            self.assertEqual(response.data['points_added'] , '10')
            facility =  response.data['facility']   
            self.dataval={
                "feedback_category": "Quality of Service",
                "feedback_subcategory": 'Occupation',
                "time_action": timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                "score": 3,
                "image_url": "",
                "text": "yeee",
                "user_lat": 10.1,
                "user_lon": 12.1,
                "facility": facility
            }
            response = self.client.post(self.carparkvalidateurl,self.dataval,format='json')
            self.assertEqual(response.status_code ,  status.HTTP_200_OK)
# BusStopInfoView view is a very complex endpoint to test - later

class SimpleEndpointsAPIViewTest(APITestCase):
    
    clienturl = reverse('shop')
    def tearDown(self): # django does this automatically 
        pass 
    def setUp(self): 
        
        #create a user (not a client) 
        self.user = Client.objects.create_user(username='placeholder', password='password', email='leoremic@gmail.com')
        #create a token 
        access_token = AccessToken.for_user(self.user)
        # Assign the JWT token to the authorization header of our client
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(access_token))
        
    def test_get_endpoints_autheticated(self):
        endpoints = ['facilitytype','structfeed','shop','item','bus','rail', 'agency', 'route','calendardate','trips','stoptimes','calendar','stops','shapes','feedgiven','feedval']  # Add other endpoint names here
        for endpoint in endpoints:
            url = reverse(endpoint)
            response = self.client.get(url)
            self.assertEqual(response.status_code ,  status.HTTP_403_FORBIDDEN)
            # Add more assertions or checks for the response as needed
        for endpoint in endpoints:
            url = reverse(endpoint)
            self.client.credentials(HTTP_AUTHORIZATION='')
            response = self.client.get(url)
            self.assertEqual(response.status_code ,  status.HTTP_401_UNAUTHORIZED)
            # Add more assertions or checks for the response as needed    
        for endpoint in endpoints:
                           
            url = reverse(endpoint)
            self.user = Client.objects.create_user(username='testuser'+endpoint, password='password', email='joao@hotmail.com')
            self.user.is_staff=True
            self.user.save()
            access_token = AccessToken.for_user(self.user)
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(access_token))
            response = self.client.get(url)
            self.assertEqual(response.status_code ,  status.HTTP_200_OK)


class FeedbackcatViewAPIViewTest(APITestCase):
    
        clienturl = reverse('category')

        def tearDown(self): # django does this automatically 
            pass 
        def setUp(self): 
        
            #create a user (not a client) 
            self.user = Client.objects.create_user(username='testuser', password='password', email='joao@hotmail.com')
            self.user.is_staff=True
            self.user.save()
            access_token = AccessToken.for_user(self.user)
            # Assign the JWT token to the authorization header of our client
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(access_token))
            self.data = [
            {
                "feedback_category": "Quality of Service",
                "feedback_category_short": "QOS",
                "color_red": 53,
                "color_green": 182,
                "color_blue": 51,
                "imageurl": "qos.png"
            },
            {
                "feedback_category": "Security",
                "feedback_category_short": "SEC",
                "color_red": 255,
                "color_green": 0,
                "color_blue": 0,
                "imageurl": "lock.png"
            },
            {
                "feedback_category": "Maintenance",
                "feedback_category_short": "MTN",
                "color_red": 45,
                "color_green": 207,
                "color_blue": 242,
                "imageurl": "maintenance.png"
            },
            {
                "feedback_category": "General",
                "feedback_category_short": "GEN",
                "color_red": 0,
                "color_green": 0,
                "color_blue": 0,
                "imageurl": ""
            }
            ]
            
        
        def test_create_feedbackcat(self):
            response = self.client.post(self.clienturl,self.data,format='json')
            # print('response.data')
            self.assertEqual(response.status_code ,  status.HTTP_200_OK)
            i=0
            
            for dic in response.data:
                self.assertEqual(dic['feedback_category'] , self.data[i]['feedback_category'])
                self.assertEqual(dic["feedback_category_short"] , self.data[i]["feedback_category_short"])

                i=i+1
             
class FeedbacksubcatViewAPIViewTest(APITestCase):
        def tearDown(self): # django does this automatically 
            pass 
          
        clienturl = reverse('subcategory')

        def setUp(self): 
        
            #create a user (not a client) 
            self.user = Client.objects.create_user(username='testuser', password='password', email='joao@hotmail.com')
            self.user.is_staff=True
            self.user.save()
            access_token = AccessToken.for_user(self.user)
            # Assign the JWT token to the authorization header of our client
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(access_token))
            self.data=[
            {
                "feedback_subcategory": "Occupation",
                "feedback_subcategory_short": "OCP",
                "color_red": 73,
                "color_green": 169,
                "color_blue": 88,
                "imageurl": "crowd.png"
            },
            {
                "feedback_subcategory": "Costumer-service",
                "feedback_subcategory_short": "CS",
                "color_red": 69,
                "color_green": 222,
                "color_blue": 56,
                "imageurl": "support.png"
            },
            {
                "feedback_subcategory": "Cleanliness",
                "feedback_subcategory_short": "CLN",
                "color_red": 107,
                "color_green": 255,
                "color_blue": 149,
                "imageurl": "cleaning.png"
            },
            {
                "feedback_subcategory": "Comfort",
                "feedback_subcategory_short": "CMF",
                "color_red": 187,
                "color_green": 255,
                "color_blue": 202,
                "imageurl": "sofa.png"
            },
            {
                "feedback_subcategory": "Service delay",
                "feedback_subcategory_short": "SD",
                "color_red": 172,
                "color_green": 254,
                "color_blue": 195,
                "imageurl": "clock.png"
            },
            {
                "feedback_subcategory": "Personal safety",
                "feedback_subcategory_short": "PSF",
                "color_red": 178,
                "color_green": 42,
                "color_blue": 42,
                "imageurl": "protection.png"
            },
            {
                "feedback_subcategory": "Belongings safety",
                "feedback_subcategory_short": "BSF",
                "color_red": 255,
                "color_green": 77,
                "color_blue": 0,
                "imageurl": "luggage.png"
            },
            {
                "feedback_subcategory": "Lightening",
                "feedback_subcategory_short": "ILU",
                "color_red": 255,
                "color_green": 230,
                "color_blue": 0,
                "imageurl": "lamp.png"
            },
            {
                "feedback_subcategory": "Driving",
                "feedback_subcategory_short": "DRV",
                "color_red": 255,
                "color_green": 168,
                "color_blue": 0,
                "imageurl": "hands.png"
            },
            {
                "feedback_subcategory": "Infrastructure state",
                "feedback_subcategory_short": "INF",
                "color_red": 0,
                "color_green": 56,
                "color_blue": 255,
                "imageurl": "infrastructure.png"
            },
            {
                "feedback_subcategory": "Road state",
                "feedback_subcategory_short": "RoS",
                "color_red": 77,
                "color_green": 116,
                "color_blue": 255,
                "imageurl": "road.png"
            },
            {
                "feedback_subcategory": "Obstacles",
                "feedback_subcategory_short": "OBS",
                "color_red": 133,
                "color_green": 152,
                "color_blue": 255,
                "imageurl": "barrier.png"
            },
            {
                "feedback_subcategory": "Accessibility",
                "feedback_subcategory_short": "ACS",
                "color_red": 173,
                "color_green": 206,
                "color_blue": 255,
                "imageurl": "import.png"
            },
            {
                "feedback_subcategory": "Classification",
                "feedback_subcategory_short": "CLA",
                "color_red": 0,
                "color_green": 0,
                "color_blue": 0,
                "imageurl": ""
            }
            ]
            
     
        def test_create_feedbacksubcat(self):
            response = self.client.post(self.clienturl,self.data,format='json')
            self.assertEqual(response.status_code ,  status.HTTP_200_OK)
            i=0
            for dic in response.data:
                self.assertEqual(dic['feedback_subcategory'] , self.data[i]['feedback_subcategory'])
                self.assertEqual(dic["feedback_subcategory_short"] , self.data[i]["feedback_subcategory_short"])

                i=i+1

class FacilitytypeViewAPIViewTest(APITestCase):
    
        clienturl = reverse('facilitytype')
        def tearDown(self): # django does this automatically 
            pass 
        def setUp(self): 
        
            #create a user (not a client) 
            self.user = Client.objects.create_user(username='testuser', password='password', email='joao@hotmail.com')
            self.user.is_staff=True
            self.user.save()
            access_token = AccessToken.for_user(self.user)
            # Assign the JWT token to the authorization header of our client
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(access_token))
            self.data =  [  {
                    "facility_type_id": 0,
                    "facility_type_name": "Tram, Streetcar, Light rail"
                },
                {
                    "facility_type_id": 1,
                    "facility_type_name": "Subway, Metro"
                },
                {
                    "facility_type_id": 2,
                    "facility_type_name": "Rail"
                },
                {
                    "facility_type_id": 3,
                    "facility_type_name": "Bus"
                },
                {
                    "facility_type_id": 4,
                    "facility_type_name": "Ferry"
                },
                {
                    "facility_type_id": 5,
                    "facility_type_name": "Cable tram"
                },
                {
                    "facility_type_id": 6,
                    "facility_type_name": "Aerial lift, suspended cable car"
                },
                {
                    "facility_type_id": 7,
                    "facility_type_name": "Funicular"
                },
                {
                    "facility_type_id": 8,
                    "facility_type_name": "Car Park"
                },
                {
                    "facility_type_id": 11,
                    "facility_type_name": "Trolleybus"
                },
                {
                    "facility_type_id": 12,
                    "facility_type_name": "Monorail"
                },
                {
                    "facility_type_id": 33,
                    "facility_type_name": "Bus stop"
                },
                {
                    "facility_type_id": 22,
                    "facility_type_name": "Rail station"
                },
                {
                    "facility_type_id": 13,
                    "facility_type_name": "Mobility Station"
                }
                ]
            
        
        def test_create_facilitytype(self):
            response = self.client.post(self.clienturl,self.data,format='json')
            self.assertEqual(response.status_code ,  status.HTTP_200_OK)
            i=0
            for dic in response.data:
                self.assertEqual(dic['facility_type_id'] , self.data[i]['facility_type_id'])
                self.assertEqual(dic["facility_type_name"] , self.data[i]["facility_type_name"])

                i=i+1
                    
class FeedbackstructAPIViewTest(APITestCase):
        clienturl = reverse('structfeed')
        facilitytypeurl = reverse('facilitytype')
        subcategoryurl = reverse('subcategory')
        categoryurl = reverse('category')

        def tearDown(self): # django does this automatically 
            pass 
        def setUp(self): 

            #create a user (not a client) 
            self.user = Client.objects.create_user(username='testuser', password='password', email='joao@hotmail.com')
            self.user.is_staff=True
            self.user.save()
            access_token = AccessToken.for_user(self.user)
            # Assign the JWT token to the authorization header of our client
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(access_token))
            self.datacreateFacilityType = [
                {
                    "facility_type_id": 0,
                    "facility_type_name": "Tram, Streetcar, Light rail"
                },
                {
                    "facility_type_id": 1,
                    "facility_type_name": "Subway, Metro"
                },
                {
                    "facility_type_id": 2,
                    "facility_type_name": "Rail"
                },
                {
                    "facility_type_id": 3,
                    "facility_type_name": "Bus"
                },
                {
                    "facility_type_id": 4,
                    "facility_type_name": "Ferry"
                },
                {
                    "facility_type_id": 5,
                    "facility_type_name": "Cable tram"
                },
                {
                    "facility_type_id": 6,
                    "facility_type_name": "Aerial lift, suspended cable car"
                },
                {
                    "facility_type_id": 7,
                    "facility_type_name": "Funicular"
                },
                {
                    "facility_type_id": 8,
                    "facility_type_name": "Car Park"
                },
                {
                    "facility_type_id": 11,
                    "facility_type_name": "Trolleybus"
                },
                {
                    "facility_type_id": 12,
                    "facility_type_name": "Monorail"
                },
                {
                    "facility_type_id": 33,
                    "facility_type_name": "Bus stop"
                },
                {
                    "facility_type_id": 22,
                    "facility_type_name": "Rail station"
                },
                {
                    "facility_type_id": 13,
                    "facility_type_name": "Mobility Station"
                }
                ]
            self.datacreateFeedbackcategory = [
            {
                "feedback_category": "Quality of Service",
                "feedback_category_short": "QOS",
                "color_red": 53,
                "color_green": 182,
                "color_blue": 51,
                "imageurl": "qos.png"
            },
            {
                "feedback_category": "Security",
                "feedback_category_short": "SEC",
                "color_red": 255,
                "color_green": 0,
                "color_blue": 0,
                "imageurl": "lock.png"
            },
            {
                "feedback_category": "Maintenance",
                "feedback_category_short": "MTN",
                "color_red": 45,
                "color_green": 207,
                "color_blue": 242,
                "imageurl": "maintenance.png"
            },
            {
                "feedback_category": "General",
                "feedback_category_short": "GEN",
                "color_red": 0,
                "color_green": 0,
                "color_blue": 0,
                "imageurl": ""
            }
            ]
            self.datacreateFeedbacksubcategory = [
            {
                "feedback_subcategory": "Occupation",
                "feedback_subcategory_short": "OCP",
                "color_red": 73,
                "color_green": 169,
                "color_blue": 88,
                "imageurl": "crowd.png"
            },
            {
                "feedback_subcategory": "Costumer-service",
                "feedback_subcategory_short": "CS",
                "color_red": 69,
                "color_green": 222,
                "color_blue": 56,
                "imageurl": "support.png"
            },
            {
                "feedback_subcategory": "Cleanliness",
                "feedback_subcategory_short": "CLN",
                "color_red": 107,
                "color_green": 255,
                "color_blue": 149,
                "imageurl": "cleaning.png"
            },
            {
                "feedback_subcategory": "Comfort",
                "feedback_subcategory_short": "CMF",
                "color_red": 187,
                "color_green": 255,
                "color_blue": 202,
                "imageurl": "sofa.png"
            },
            {
                "feedback_subcategory": "Service delay",
                "feedback_subcategory_short": "SD",
                "color_red": 172,
                "color_green": 254,
                "color_blue": 195,
                "imageurl": "clock.png"
            },
            {
                "feedback_subcategory": "Personal safety",
                "feedback_subcategory_short": "PSF",
                "color_red": 178,
                "color_green": 42,
                "color_blue": 42,
                "imageurl": "protection.png"
            },
            {
                "feedback_subcategory": "Belongings safety",
                "feedback_subcategory_short": "BSF",
                "color_red": 255,
                "color_green": 77,
                "color_blue": 0,
                "imageurl": "luggage.png"
            },
            {
                "feedback_subcategory": "Lightening",
                "feedback_subcategory_short": "ILU",
                "color_red": 255,
                "color_green": 230,
                "color_blue": 0,
                "imageurl": "lamp.png"
            },
            {
                "feedback_subcategory": "Driving",
                "feedback_subcategory_short": "DRV",
                "color_red": 255,
                "color_green": 168,
                "color_blue": 0,
                "imageurl": "hands.png"
            },
            {
                "feedback_subcategory": "Infrastructure state",
                "feedback_subcategory_short": "INF",
                "color_red": 0,
                "color_green": 56,
                "color_blue": 255,
                "imageurl": "infrastructure.png"
            },
            {
                "feedback_subcategory": "Road state",
                "feedback_subcategory_short": "RoS",
                "color_red": 77,
                "color_green": 116,
                "color_blue": 255,
                "imageurl": "road.png"
            },
            {
                "feedback_subcategory": "Obstacles",
                "feedback_subcategory_short": "OBS",
                "color_red": 133,
                "color_green": 152,
                "color_blue": 255,
                "imageurl": "barrier.png"
            },
            {
                "feedback_subcategory": "Accessibility",
                "feedback_subcategory_short": "ACS",
                "color_red": 173,
                "color_green": 206,
                "color_blue": 255,
                "imageurl": "import.png"
            },
            {
                "feedback_subcategory": "Classification",
                "feedback_subcategory_short": "CLA",
                "color_red": 0,
                "color_green": 0,
                "color_blue": 0,
                "imageurl": ""
            }
            ]
            self.data=[
                {
                    "facility_type": 3,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Occupation"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Costumer-service"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Cleanliness"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Comfort"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Service delay"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Personal safety"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Belongings safety"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Lightening"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Driving"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Infrastructure state"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Road state"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Obstacles"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Accessibility"
                },
                {
                    "facility_type": 3,
                    "feedback_category": "General",
                    "feedback_subcategory": "Classification"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Occupation"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Cleanliness"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Comfort"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Service delay"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Personal safety"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Belongings safety"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Lightening"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Driving"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Infrastructure state"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Road state"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Accessibility"
                },
                {
                    "facility_type": 2,
                    "feedback_category": "General",
                    "feedback_subcategory": "Classification"
                },
                {
                    "facility_type": 13,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Costumer-service"
                },
                {
                    "facility_type": 13,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Cleanliness"
                },
                {
                    "facility_type": 13,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Comfort"
                },
                {
                    "facility_type": 13,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Service delay"
                },
                {
                    "facility_type": 13,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Personal safety"
                },
                {
                    "facility_type": 13,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Belongings safety"
                },
                {
                    "facility_type": 13,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Lightening"
                },
                {
                    "facility_type": 13,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Infrastructure state"
                },
                {
                    "facility_type": 13,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Accessibility"
                },
                {
                    "facility_type": 13,
                    "feedback_category": "General",
                    "feedback_subcategory": "Classification"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Occupation"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Cleanliness"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Comfort"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Service delay"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Personal safety"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Belongings safety"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Lightening"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Infrastructure state"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Road state"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Obstacles"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Accessibility"
                },
                {
                    "facility_type": 33,
                    "feedback_category": "General",
                    "feedback_subcategory": "Classification"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Occupation"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Costumer-service"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Cleanliness"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Comfort"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Service delay"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Personal safety"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Belongings safety"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Security",
                    "feedback_subcategory": "Lightening"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Infrastructure state"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Road state"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Obstacles"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "Maintenance",
                    "feedback_subcategory": "Accessibility"
                },
                {
                    "facility_type": 22,
                    "feedback_category": "General",
                    "feedback_subcategory": "Classification"
                },
                {
                    "facility_type": 8,
                    "feedback_category": "Quality of Service",
                    "feedback_subcategory": "Occupation"
                }
                ]
        def test_create_feedbackstruct(self):
            response = self.client.post(self.facilitytypeurl,self.datacreateFacilityType,format='json')
            self.assertEqual(response.status_code ,  status.HTTP_200_OK)
            #print(response.data)
            i=0
            for dic in response.data:
                #print(i)
                self.assertEqual(dic['facility_type_id'] , self.datacreateFacilityType[i]['facility_type_id'])
                self.assertEqual(dic["facility_type_name"] , self.datacreateFacilityType[i]["facility_type_name"])
                i=i+1 
            response = self.client.post(self.subcategoryurl,self.datacreateFeedbacksubcategory,format='json')
            self.assertEqual(response.status_code ,  status.HTTP_200_OK)
            i=0
            for dic in response.data:
                self.assertEqual(dic['feedback_subcategory'] , self.datacreateFeedbacksubcategory[i]['feedback_subcategory'])
                self.assertEqual(dic["feedback_subcategory_short"] , self.datacreateFeedbacksubcategory[i]["feedback_subcategory_short"])
                i=i+1
            response = self.client.post(self.categoryurl,self.datacreateFeedbackcategory,format='json')
            self.assertEqual(response.status_code ,  status.HTTP_200_OK)
            i=0
            for dic in response.data:
                self.assertEqual(dic['feedback_category'] , self.datacreateFeedbackcategory[i]['feedback_category'])
                self.assertEqual(dic["feedback_category_short"] , self.datacreateFeedbackcategory[i]["feedback_category_short"])
                i=i+1

            response = self.client.post(self.clienturl,self.data,format='json')
            #print(response.data)

            self.assertEqual(response.status_code ,  status.HTTP_200_OK)
            i=0
            for dic in response.data:
                self.assertEqual(dic['facility_type'] , self.data[i]['facility_type'])
                self.assertEqual(dic["feedback_subcategory"] , self.data[i]["feedback_subcategory"])
                self.assertEqual(dic["feedback_category"] , self.data[i]["feedback_category"])
                i=i+1

            
                
class ShopViewAPIViewTest(APITestCase):
    
        clienturl = reverse('shop')

        def tearDown(self): # django does this automatically 
            pass 
        def setUp(self): 
        
            #create a user (not a client) 
            self.user = Client.objects.create_user(username='testuser', password='password', email='joao@hotmail.com')
            self.user.is_staff=True
            self.user.save()
            access_token = AccessToken.for_user(self.user)
            # Assign the JWT token to the authorization header of our client
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(access_token))
            self.data = [
                {
                    "name": "CAFE DO RIO"
                },
                {
                    "name": "RESTAURANTE DO ZE"
                }
                ]
            
        
        def test_create_shop(self):
            response = self.client.post(self.clienturl,self.data,format='json')
            self.assertEqual(response.status_code ,  status.HTTP_200_OK)
            i=0
            for dic in response.data:
                self.assertEqual(dic['name'] , self.data[i]['name'])

                i=i+1


class ItemAPIViewTest(APITestCase):
    
        itemurl = reverse('item')
        shopurl= reverse('shop')

        def tearDown(self): # django does this automatically 
            pass 
        
        def setUp(self): 
        
            #create a user (not a client) 
            self.user = Client.objects.create_user(username='testuser', password='password', email='joao@hotmail.com')
            self.user.is_staff=True
            self.user.save()
            access_token = AccessToken.for_user(self.user)
            # Assign the JWT token to the authorization header of our client
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(access_token))
            self.shopdata = [
                {
                    "shop_id": 1,
                    "name": "CAFE DO RIO"
                },
                {
                    "shop_id": 2,
                    "name": "RESTAURANTE DO ZE"
                }
                ]
            self.itemdata=[
                {
                "category": "BEBIDAS",
                "name": "CAFE",
                "price": 300,
                "shop": 1,
                "quantity": 20
                },
                {
                "category": "PRATOS",
                "name": "BITOQUE",
                "price": 1000,
                "shop": 1,
                "quantity": 1
                },
                {
                "category": "BEBIDAS",
                "name": "COCA COLA 300ml",
                "price": 400,
                "shop": 1,
                "quantity": 20
                },
                {
                "category": "BEBIDAS",
                "name": "Pastel de nata",
                "price": 200,
                "shop": 1,
                "quantity": 20
                },
                {
                "category": "BEBIDAS",
                "name": "Croissant",
                "price": 100,
                "shop": 1,
                "quantity": 20
                },
                {
                "category": "BOLOS",
                "name": "PAO DE LO",
                "price": 1000,
                "shop": 2,
                "quantity": 2
                }
                ]
            
        
        def test_create_item(self):
            
            response = self.client.post(self.shopurl,self.shopdata,format='json')
            self.assertEqual(response.status_code ,  status.HTTP_200_OK)
            i=0
            for dic in response.data:
                self.assertEqual(dic['name'] , self.shopdata[i]['name'])
                self.assertEqual(dic["shop_id"] , self.shopdata[i]["shop_id"])
                i=i+1
            response = self.client.post(self.itemurl,self.itemdata,format='json')
            self.assertEqual(response.status_code ,  status.HTTP_200_OK)
            i=0
            for dic in response.data:
                self.assertEqual(dic['name'] , self.itemdata[i]['name'])
                self.assertEqual(dic["shop"] , self.itemdata[i]["shop"])
                i=i+1


            
            

class RailAPIViewTest(APITestCase):
    
        railurl = reverse('rail')
        facilitytypeurl = reverse('facilitytype')

        
        def tearDown(self): # django does this automatically 
            pass 
        
        def setUp(self): 
            
            #create a user (not a client) 
            self.user = Client.objects.create_user(username='testuser', password='password', email='joao@hotmail.com')
            self.user.is_staff=True
            self.user.save()
            access_token = AccessToken.for_user(self.user)
            # Assign the JWT token to the authorization header of our client
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(access_token))
            self.raildata= [{
            "facility": "Rail1111",
            "unit_number": "Unit Number",
            "registration_plate": "Registration Plate",
            "bus_desc": "Bus Description",
            "capacity": 30,
            "standing_capacity": 10,
            "seats": 20
            },
            {
            "facility": "Rail2222",
            "unit_number": "Unit Number",
            "registration_plate": "Registration Plate",
            "bus_desc": "Bus Description",
            "capacity": 10,
            "standing_capacity": 30,
            "seats": 20
            }
            ]
            self.facilitytypedata =  [  {
                    "facility_type_id": 0,
                    "facility_type_name": "Tram, Streetcar, Light rail"
                },
                {
                    "facility_type_id": 1,
                    "facility_type_name": "Subway, Metro"
                },
                {
                    "facility_type_id": 2,
                    "facility_type_name": "Rail"
                },
                {
                    "facility_type_id": 3,
                    "facility_type_name": "Bus"
                },
                {
                    "facility_type_id": 4,
                    "facility_type_name": "Ferry"
                },
                {
                    "facility_type_id": 5,
                    "facility_type_name": "Cable tram"
                },
                {
                    "facility_type_id": 6,
                    "facility_type_name": "Aerial lift, suspended cable car"
                },
                {
                    "facility_type_id": 7,
                    "facility_type_name": "Funicular"
                },
                {
                    "facility_type_id": 8,
                    "facility_type_name": "Car Park"
                },
                {
                    "facility_type_id": 11,
                    "facility_type_name": "Trolleybus"
                },
                {
                    "facility_type_id": 12,
                    "facility_type_name": "Monorail"
                },
                {
                    "facility_type_id": 33,
                    "facility_type_name": "Bus stop"
                },
                {
                    "facility_type_id": 22,
                    "facility_type_name": "Rail station"
                },
                {
                    "facility_type_id": 13,
                    "facility_type_name": "Mobility Station"
                }
                ]
        
        def test_create_rail(self):
            response = self.client.post(self.facilitytypeurl,self.facilitytypedata,format='json')
            self.assertEqual(response.status_code ,  status.HTTP_200_OK)
            i=0
            for dic in response.data:
                self.assertEqual(dic['facility_type_id'] , self.facilitytypedata[i]['facility_type_id'])
                self.assertEqual(dic["facility_type_name"] , self.facilitytypedata[i]["facility_type_name"])
                i=i+1
            response = self.client.post(self.railurl,self.raildata,format='json')
            self.assertEqual(response.status_code ,  status.HTTP_200_OK)
            self.assertEqual(response.data['status'], 'sucess')

class BusAPIViewTest(APITestCase):
    
        busurl = reverse('bus')
        facilitytypeurl = reverse('facilitytype')

        
        def tearDown(self): # django does this automatically 
            pass 
        
        def setUp(self): 
            
            #create a user (not a client) 
            self.user = Client.objects.create_user(username='testuser', password='password', email='joao@hotmail.com')
            self.user.is_staff=True
            self.user.save()
            access_token = AccessToken.for_user(self.user)
            # Assign the JWT token to the authorization header of our client
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(access_token))
            self.busdata= [{
            "facility": "Bus1asas111",
            "unit_number": "Unit Number",
            "registration_plate": "Registration Plate",
            "bus_desc": "Bus Description",
            "capacity": 30,
            "standing_capacity": 10,
            "seats": 20
            },
            {
            "facility": "aaa",
            "unit_number": "Unit Number",
            "registration_plate": "Registration Plate",
            "bus_desc": "Bus Description",
            "capacity": 10,
            "standing_capacity": 30,
            "seats": 20
            }
            ]
            self.facilitytypedata =  [  {
                    "facility_type_id": 0,
                    "facility_type_name": "Tram, Streetcar, Light rail"
                },
                {
                    "facility_type_id": 1,
                    "facility_type_name": "Subway, Metro"
                },
                {
                    "facility_type_id": 2,
                    "facility_type_name": "Rail"
                },
                {
                    "facility_type_id": 3,
                    "facility_type_name": "Bus"
                },
                {
                    "facility_type_id": 4,
                    "facility_type_name": "Ferry"
                },
                {
                    "facility_type_id": 5,
                    "facility_type_name": "Cable tram"
                },
                {
                    "facility_type_id": 6,
                    "facility_type_name": "Aerial lift, suspended cable car"
                },
                {
                    "facility_type_id": 7,
                    "facility_type_name": "Funicular"
                },
                {
                    "facility_type_id": 8,
                    "facility_type_name": "Car Park"
                },
                {
                    "facility_type_id": 11,
                    "facility_type_name": "Trolleybus"
                },
                {
                    "facility_type_id": 12,
                    "facility_type_name": "Monorail"
                },
                {
                    "facility_type_id": 33,
                    "facility_type_name": "Bus stop"
                },
                {
                    "facility_type_id": 22,
                    "facility_type_name": "Rail station"
                },
                {
                    "facility_type_id": 13,
                    "facility_type_name": "Mobility Station"
                }
                ]
        
        def test_create_bus(self):
            response = self.client.post(self.facilitytypeurl,self.facilitytypedata,format='json')
            self.assertEqual(response.status_code ,  status.HTTP_200_OK)
            i=0
            for dic in response.data:
                self.assertEqual(dic['facility_type_id'] , self.facilitytypedata[i]['facility_type_id'])
                self.assertEqual(dic["facility_type_name"] , self.facilitytypedata[i]["facility_type_name"])
                i=i+1
            response = self.client.post(self.busurl,self.busdata,format='json')
            self.assertEqual(response.status_code ,  status.HTTP_200_OK)


            







                
            


        
