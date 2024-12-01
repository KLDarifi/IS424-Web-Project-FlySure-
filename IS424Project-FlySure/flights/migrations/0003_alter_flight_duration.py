# Generated by Django 5.1.1 on 2024-11-27 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0002_flight_airline_flight_arrival_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='duration',
            field=models.DecimalField(decimal_places=2, default='250', max_digits=10),
        ),
    ]
