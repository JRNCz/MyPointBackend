from django.test import SimpleTestCase
from django.urls import reverse, resolve 
from mypointapi.views import ClientView
from mypointapi.views import ClientDetailedView
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

from rest_framework.test import APITestCase #API Test cases comes with http requests
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User

class ApiUrlTests(SimpleTestCase):
    
    def test_get_clients_is_resolved(self):
        url = reverse('client') 
        self.assertEquals(resolve(url).func.view_class, ClientView )
        
    def test_get_token_is_resolved(self):
        url = reverse('token_obtain_pair')
        self.assertEquals(resolve(url).func.view_class, TokenObtainPairView )
        
        
    def test_get_token_refresh_is_resolved(self):
        url = reverse('token_refresh')

        self.assertEquals(resolve(url).func.view_class, TokenRefreshView )
        
    def test_get_detailed_clients_is_resolved(self):
        url = reverse('detailedclient', args=[1]) # test with pk = 1 
        self.assertEquals(resolve(url).func.view_class, ClientDetailedView )
        

class ClientAPIViewTest(APITestCase):
    url = reverse('client')
    # endpoints are protected need to send a token
    print(url)
    
    def setUp(self):
        #create a user (not a client) 
        self.user = User.objects.create_user(username='testadmin', password='password')
        #create a token 
        self.token = Token.objects.create(user = self.user)
        #assign the token to autorization header to our client
        self.client.credentials(HTTP_AUTHORIZATION ='Token ' + self.token.key)
        
    
    def tearDown(self): # django does this automatically 
        pass 
    
    def test_get_clients_autheticated(self):
        #create a get request that requests to "clients" endpoint
        response = self.client.get(self.url)
        #confirm if the get request outputs a 200 OK 
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        
    # Test clients requests without authorization    
    def test_get_clients_un_authenticated(self):
        self.client.force_authenticate(user = None, token = None)   
        response = self.client.get(self.url)  
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_post_customer_autheticated(self): 
        
        data =   {  
            "username" : "marco_gomes",
            "user_id" : 102323,
            "points" : 55,
            "password" : "owyGEWjn",
            "last_login" : "2022-01-27T15:29:27.579742Z",
            "time_created" : "2022-01-27T15:29:27.579742Z",
            "email" : "marcoeleormic@gmail.com",
            "reputation" : 0,
            "level" :  10
        }
        
        response = self.client.post(self.url,data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user_id'], '102323')

        
class ClientDetailAPIViewTest(APITestCase):
    
    url = reverse('client')
    clienturl=reverse('detailedclient' , args= [302323])
        

    def setUp(self): 
        
         #create a user (not a client) 
        self.user = User.objects.create_user(username='testadmin', password='password')
        #create a token 
        self.token = Token.objects.create(user = self.user)
        #assign the token to autorization header to our client
        self.client.credentials(HTTP_AUTHORIZATION ='Token ' + self.token.key)
        
        data =  {  
            "username" : "leandro",
            "user_id" : 302323,
            "points" : 11,
            "password" : "fdfddf",
            "last_login" : "2022-01-27T15:29:27.579742Z",
            "time_created" : "2022-01-27T15:29:27.579742Z",
            "email" : "leo1999@gmail.com",
            "reputation" : 23,
            "level" : 77
        }
        
        response = self.client.post(self.url,data, format = 'json')
         
    def test_get_customer_authenticated(self):
        #create a get request that requests to "clients" endpoint
        response = self.client.get(self.clienturl)
        #confirm if the get request outputs a 200 OK 
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['user_id'], '302323' )

    def test_get_customer_un_authenticated(self):
        self.client.force_authenticate(user = None, token = None)   
        response = self.client.get(self.clienturl)
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)  
    
    def test_delete_customer_authenticated(self):
        
        response = self.client.delete(self.clienturl)
        self.assertEqual(response.status_code ,  status.HTTP_202_ACCEPTED )
        

