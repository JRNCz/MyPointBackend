from django.urls import path
from mypointapi import views as api_views
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

 


urlpatterns = [
    path('clients/', api_views.ClientView.as_view(), name = "client"),
    path('clients/<int:pk>/', api_views.ClientDetailedView.as_view(), name = "detailedclient" ),
    path('token/', TokenObtainPairView.as_view(), name = "token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name = "token_refresh"),
    path('facilities/', api_views.FacilityView.as_view(), name = "facilities"),
    path('facilities/<str:facilityType>', api_views.FacilityDetailedView.as_view(), name = "detailedfacility"),
    path('feedback/', api_views.FeedbackView.as_view(), name = "feedback"),
    path('feedback/category', api_views.FeedbackcatView.as_view(), name = "category"),
    path('feedback/subcategory', api_views.FeedbacksubcatView.as_view(), name = "subcategory"),
    path('stops/', api_views.StopsView.as_view(), name = "stops"),
    path('shop/', api_views.ShopView.as_view(), name = "shop"),
    path('item/', api_views.ItemView.as_view(), name = "item"),
    path('bus/', api_views.BusView.as_view(), name = "bus"),
    path('rail/', api_views.RailView.as_view(), name = "rail"),
    path('facilitytype/', api_views.FacilityTypeView.as_view(), name = "facilitytype"),
    path('facilitytype/<int:pk>/', api_views.FacilityTypeDetailedView.as_view(), name = "detailedfacilitytype"),
    path('agency/', api_views.AgencyView.as_view(), name = "agency"),
    path('route/', api_views.RouteView.as_view(), name = "route"),
    path('calendardate/', api_views.CalendarDatesView.as_view(), name = "calendardate"),
    path('trip/', api_views.TripView.as_view(), name = "trips"),
    path('stoptimes/', api_views.StopTimesView.as_view(), name = "stoptimes"),
    path('calendar/', api_views.CalendarView.as_view(), name = "calendar"),
    path('shapes/', api_views.ShapesView.as_view(), name = "shapes"),
    path('feedbackgiven/', api_views.FeedbackGivenView.as_view(), name = "feedgiven"),
    path('feedbackvalidation/', api_views.FeedbackValidationView.as_view(), name = "feedval"),
    path('categories/<str:facilityType>/', api_views.CategoriesView.as_view(), name = "categorycheck"),
    path('feedbackstruct/', api_views.FeedbackstructView.as_view(), name = "structfeed"),
    path('item/<int:pk>/', api_views.ItemDetailedView.as_view(), name = "itemdetailed"),
    path('client/account/',api_views.AccountInfoView.as_view(), name = "accountinfo"),
    path('feedback/carpark', api_views.CarParkFeedbackView.as_view(), name = "carparkfeed"),
    path('feedback/carpark/validate', api_views.CarParkFeedbackValidateView.as_view(), name = "carparkvalidate"),
    path('busstop/information/<str:pk>', api_views.BusStopInfoView.as_view(), name = "busstop")




    



    
    









    


]
