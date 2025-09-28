# gpsinfo/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import GPSLocation, GPSLatest
from .serializers import GPSLocationSerializer, GPSLatestSerializer

class GPSLocationViewSet(viewsets.ModelViewSet):
    queryset = GPSLocation.objects.all()
    serializer_class = GPSLocationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only show locations for the authenticated user
        return GPSLocation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Save the GPSLocation
        gps_location = serializer.save(user=self.request.user)
        
        # Update or create GPSLatest
        GPSLatest.objects.update_or_create(
            user=self.request.user,
            defaults={
                'latitude': gps_location.latitude,
                'longitude': gps_location.longitude,
                'timestamp': gps_location.timestamp,
                'altitude': gps_location.altitude,
                'accuracy': gps_location.accuracy,
            }
        )

    @action(detail=False, methods=['get'], url_path='latest')
    def get_latest_locations(self, request):
        """
        Fetch the latest GPS location for all users.
        """
        user = request.user
        if user.is_authenticated:
            # Only show latest locations for the authenticated user
            latest_locations = GPSLatest.objects.all()
            if latest_locations.exists():
                serializer = GPSLatestSerializer(latest_locations, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"message": "No location data available"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['get'], url_path='my-locations')
    def get_my_locations(self, request):
        """
        Fetch all GPS locations for the authenticated user.
        """
        user = request.user
        if user.is_authenticated:
            locations = GPSLocation.objects.filter(user=user).order_by('-timestamp')
            serializer = GPSLocationSerializer(locations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)