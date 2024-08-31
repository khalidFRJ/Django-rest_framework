from rest_framework import serializers
from my_api.models import Guest , Movie , Reservation


class MovieSerialiser(serializers.ModelSerializer):
    class Meta : 
        model = Movie
        fields = '__all__'


class GuestSerializer(serializers.ModelSerializer):
    class Meta : 
        model = Guest
        fields = ['pk' , 'reservation' , 'name', 'mobile']    


class ReservationSerialiser(serializers.ModelSerializer):
    class Meta : 
        model = Reservation
        fields = '__all__'  