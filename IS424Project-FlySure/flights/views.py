from django.shortcuts import render, redirect, get_object_or_404
from .models import Flight, Passenger
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import FlightForm
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy


def flights_list(request):
    flights = Flight.objects.all()
    return render(request, "flights/flights_list.html", {"flights": flights})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("flights_list")  
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})
    return render(request, "login.html")

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password=password, email=email)
            return redirect("login")
        else:
            return render(request, "register.html", {"error": "Username already exists"})
    return render(request, "register.html")

@login_required
def flight_detail(request, flight_id):
    # Get the specific flight by ID or return 404 if not found
    flight = get_object_or_404(Flight, id=flight_id)

    passenger, created = Passenger.objects.get_or_create(username=request.user.username)

    already_booked = passenger.flights.filter(id=flight_id).exists()

    if request.method == "POST" and not already_booked:
        passenger.flights.add(flight)
        return redirect("flight_detail", flight_id=flight.id) 
    
    return render(request, "flights/flight_detail.html", {
        "flight": flight,
        "already_booked": already_booked
    })

@login_required
def booked_flights(request):
    passenger = Passenger.objects.filter(
        first_name=request.user.first_name, last_name=request.user.last_name
    ).first()
    flights = passenger.flights.all() if passenger else []
    return render(request, "flights/booked_flights.html", {"flights": flights})

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
@login_required
def add_flight(request):
    if request.method == "POST":
        form = FlightForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("flights_list")
    else:
        form = FlightForm()
    return render(request, "flights/add_flight.html", {"form": form})

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
@login_required
def add_flight(request):
    if request.method == "POST":
        form = FlightForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("flights_list")
    else:
        form = FlightForm()
    return render(request, "flights/add_flight.html", {"form": form})

class FlightUpdateView(UpdateView):
    model = Flight
    fields = ['origin', 'destination', 'duration', 'price', 'departure_time', 'arrival_time']
    template_name = "flights/edit_flight.html"
    success_url = reverse_lazy("flights_list")

class FlightDeleteView(DeleteView):
    model = Flight
    template_name = "flights/delete_flight.html"
    success_url = "/flights/"