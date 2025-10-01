# rbackend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework.routers import DefaultRouter
from gpsinfo.views import GPSLocationViewSet
from pages.views import GpsTestView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'gpslocations', GPSLocationViewSet, basename='gpslocation')

urlpatterns = [
    # Django Templates Interface
    path('', include('pages.urls', namespace='pages')),
    path('gpstest/', GpsTestView.as_view(), name='gpstest'),
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('pages:index'), name='home'),
    
    path('accounts/', include('allauth.urls')),  # Allauth for web
    path('events/', include('events.urls', namespace='events')),
        
    # REST API
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Mobile Auth Endpoints (New dedicated app)
    path('api/auth/', include('mobile_auth.urls')),  # Clean separation!
]