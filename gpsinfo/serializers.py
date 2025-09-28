# gpsinfo/serializers.py
from rest_framework import serializers
from .models import GPSLocation, GPSLatest

class GPSLocationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = GPSLocation
        fields = ['id', 'latitude', 'longitude', 'timestamp', 'altitude', 'accuracy', 'username']
        read_only_fields = ['timestamp', 'username']

class GPSLatestSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = GPSLatest
        fields = ['username', 'latitude', 'longitude', 'timestamp', 'altitude', 'accuracy']
        read_only_fields = ['username', 'timestamp']