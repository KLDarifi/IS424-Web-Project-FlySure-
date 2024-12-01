from django.db import models

class Airport(models.Model):
    code = models.CharField(max_length = 3)
    city = models.CharField(max_length = 64)

    def __str__(self):
        return f"{self.city} ({self.code})"
    

class Flight(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.DecimalField(max_digits=10, decimal_places=2, default="250") #In minutes
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    departure_time = models.DateTimeField(null=True)
    arrival_time = models.DateTimeField(null=True)
    airline = models.CharField(max_length=64, null=True)

    def __str__(self):
        return f"{self.origin} to {self.destination} - Duration: {self.duration} minutes"
    
class Passenger(models.Model):
    username = models.CharField(max_length=64, unique=True)  #Unique username
    flights = models.ManyToManyField("Flight", related_name="passengers") #Many-to-Many relationship with flights

    def __str__(self):
        return self.username