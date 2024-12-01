from django.urls import path
from . import views

urlpatterns = [
    path("", views.flights_list, name="flights_list"),#Main page for loggedin users
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path("add/", views.add_flight, name="add_flight"),
    path("<int:pk>/edit/", views.FlightUpdateView.as_view(), name="edit_flight"),
    path("<int:pk>/delete/", views.FlightDeleteView.as_view(), name="delete_flight"),
    path("<int:flight_id>/", views.flight_detail, name="flight_detail"),
]
