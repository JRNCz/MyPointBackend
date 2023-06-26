from rest_framework import serializers
from mypointbusiness.models import Feedbackstruct
from mypointbusiness.models import Feedback
from mypointbusiness.models import Feedbackcat
from mypointbusiness.models import Feedbacksubcat
from mypointbusiness.models import Carpark

from mypointbusiness.models import Client 
from mypointbusiness.models import Orders

from mypointbusiness.models import Facility
from mypointbusiness.models import Stops
from mypointbusiness.models import Bus 
from mypointbusiness.models import Item
from mypointbusiness.models import Rail
from mypointbusiness.models import Facilitytype
from mypointbusiness.models import Routes
from mypointbusiness.models import Agency
from mypointbusiness.models import CalendarDates
from mypointbusiness.models import Trips
from mypointbusiness.models import Shop
from mypointbusiness.models import StopTimes
from mypointbusiness.models import Calendar 
from mypointbusiness.models import Shapes
from mypointbusiness.models import ValidateFeedback
from mypointbusiness.models import GiveFeedback, HasFacilities

class AccoutInfoSerializer(serializers.ModelSerializer):
      class Meta:
        model = Client  
        fields = ['points', 'level','email','reputation', 'username']

class AccoutgetPointsSerializer(serializers.ModelSerializer):
      class Meta:
        model = Client  
        fields = ['points','username']
                 
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client  
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client  
        fields = '__all__'

    password = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    class Meta:
        fields = ['username', 'password','id']

    password = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    
class FacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility  
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback  
        fields = '__all__'

class FeedbackstructSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedbackstruct  
        fields = '__all__'

class StopsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stops  
        fields = '__all__'

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop  
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders  
        fields = '__all__'
        
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus 
        fields = '__all__'
        
class BusNoIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = ['unit_number', 'registration_plate', 'bus_desc', 'capacity', 'standing_capacity', 'seats']

class RailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rail
        fields = '__all__'
        
class RailNoIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rail
        fields = ['unit_number', 'registration_plate', 'bus_desc', 'capacity', 'standing_capacity', 'seats']

        
        
class FacilityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facilitytype 
        fields = '__all__'

class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = '__all__'
                
class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routes
        fields = '__all__'
        
class CalendarDatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarDates
        fields = '__all__'
    
class TripsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trips
        fields = '__all__'

class StopTimesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StopTimes
        fields = '__all__'

class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = '__all__'

class StopsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stops
        fields = '__all__'
        
class ShapesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shapes
        fields = '__all__'
        
class FeedbackGivenSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiveFeedback
        fields = '__all__'
 
class FeedbackValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValidateFeedback
        fields = '__all__'
        
class FeedbackcatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedbackcat
        fields = '__all__'

class FeedbacksubcatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedbacksubcat
        fields = '__all__'
        
    
class HasFacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HasFacilities
        fields = ['facility', 'facility_type']
          
class CategoriesInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedbackstruct  
        fields = ['facility_type']

class CarParkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carpark
        fields = '__all__'
        
class CarParkFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['user_lon', 'user_lat','feedback_category','feedback_subcategory','time_action','score','text']
        

