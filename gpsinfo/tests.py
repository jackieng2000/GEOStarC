from rest_framework.test import APITestCase
from .models import GPSLocation

class GPSLocationTests(APITestCase):
    def test_create_gps_location(self):
        response = self.client.post('/api/gpslocations/', {
            'latitude': 40.7128,
            'longitude': -74.0060,
            'timestamp': '2025-08-12T12:00:00Z'
        })
        self.assertEqual(response.status_code, 201)