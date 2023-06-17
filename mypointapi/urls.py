from django.urls import path
from mypointapi import views as api_views
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

 


urlpatterns = [
    path('clients/', api_views.ClientView.as_view(), name = "client"),
    path('clients/<int:pk>/', api_views.ClientDetailedView.as_view(), name = "detailedclient" ),
    path('token/', TokenObtainPairView.as_view(), name = "token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name = "token_refresh"),
    path('facilities/', api_views.FacilityView.as_view(), name = "logout"),
    path('feedback/', api_views.FeedbackView.as_view(), name = "feedback"),
    path('stops/', api_views.StopsView.as_view(), name = "stops"),
    path('shop/', api_views.ShopView.as_view(), name = "stops"),
    path('item/', api_views.ItemView.as_view(), name = "stops"),
    path('bus/', api_views.BusView.as_view(), name = "stops"),
    path('rail/', api_views.RailView.as_view(), name = "stops"),
    path('facilitytype/', api_views.FacilityTypeView.as_view(), name = "stops"),
    path('agency/', api_views.AgencyView.as_view(), name = "stops"),
    path('route/', api_views.RouteView.as_view(), name = "stops"),
    path('calendardate/', api_views.CalendarDatesView.as_view(), name = "stops"),
    path('trip/', api_views.TripView.as_view(), name = "stops"),
    path('stoptimes/', api_views.StopTimesView.as_view(), name = "stops"),
    path('calendar/', api_views.CalendarView.as_view(), name = "stops"),
    path('stop/', api_views.StopsView.as_view(), name = "stops"),
    path('shapes/', api_views.ShapesView.as_view(), name = "stops"),
    path('feedbackgiven/', api_views.FeedbackGivenView.as_view(), name = "stops"),
    path('feedbackvalidation/', api_views.FeedbackValidationView.as_view(), name = "stops"),
    path('categories/<str:facilityType>/', api_views.CategoriesView.as_view(), name = "category"),
    path('feedbackstruct/', api_views.FeedbackstructView.as_view(), name = "structfeed"),
    path('item/<int:pk>/', api_views.ItemDetailedView.as_view(), name = "itemdetailed"),
    path('feedback/carpark', api_views.CarParkFeedbackView.as_view(), name = "carparkfeed"),
    path('client/account/',api_views.AccountInfoView.as_view(), name = "accountinfo"),
    path('feedback/carpark', api_views.CarParkFeedbackView.as_view(), name = "carparkfeed"),
    path('feedback/carpark/validate', api_views.CarParkFeedbackValidateView.as_view(), name = "carparkfeed")



    



    
    









    


]
