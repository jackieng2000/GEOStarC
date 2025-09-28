import axios from 'axios';
import { useEffect, useState } from 'react';

// Configuration for API endpoint
const API_BASE_URL = 'http://your-backend/api'; // Replace with your backend URL

const GPSTracker = () => {
  const [status, setStatus] = useState('Initializing GPS Tracker...');

  // Function to send GPS data to the backend
  const sendGPSData = async (gpsData) => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        throw new Error('No access token found. Please log in.');
      }

      await axios.post(`${API_BASE_URL}/gpslocations/`, gpsData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      // Clear GPS data from localStorage after successful submission
      localStorage.removeItem('gpsData');
      setStatus('GPS data sent successfully');
    } catch (error) {
      console.error('Failed to send GPS data:', error.message);
      setStatus(`Error sending GPS data: ${error.message}`);
      // Store data for retry if network issue
      localStorage.setItem('gpsData', JSON.stringify(gpsData));
    }
  };

  // Effect to periodically fetch and send GPS data
  useEffect(() => {
    const interval = setInterval(() => {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const gpsData = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            altitude: position.coords.altitude || null,
            accuracy: position.coords.accuracy || null,
          };

          // Store GPS data in localStorage
          localStorage.setItem('gpsData', JSON.stringify(gpsData));
          setStatus('GPS data captured');

          // Send data to backend
          sendGPSData(gpsData);
        },
        (error) => {
          console.error('Geolocation error:', error.message);
          setStatus(`Geolocation error: ${error.message}`);
        },
        { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
      );
    }, 15000); // Every 15 seconds

    // Cleanup interval on component unmount
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: '20px', textAlign: 'center' }}>
      <h2>GPS Tracker</h2>
      <p>{status}</p>
    </div>
  );
};

export default GPSTracker;