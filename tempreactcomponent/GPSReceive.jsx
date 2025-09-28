import axios from 'axios';
import { useState, useEffect } from 'react';

// Configuration for API endpoint
const API_BASE_URL = 'http://your-backend/api'; // Replace with your backend URL

const GPSReceive = () => {
  const [userGroup, setUserGroup] = useState('');
  const [gpsRecords, setGpsRecords] = useState([]);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const fetchGPSRecords = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        throw new Error('No access token found. Please log in.');
      }

      setIsLoading(true);
      const response = await axios.get(`${API_BASE_URL}/gpslocations/latest`, {
        headers: { Authorization: `Bearer ${token}` },
        params: { user_group: userGroup || undefined },
      });

      setGpsRecords(response.data);
      setError('');
    } catch (err) {
      setError(err.message || 'Failed to fetch GPS records.');
      setGpsRecords([]);
    } finally {
      setIsLoading(false);
    }
  };

  // Fetch records every 30 seconds
  useEffect(() => {
    if (userGroup) {
      fetchGPSRecords(); // Initial fetch
      const interval = setInterval(fetchGPSRecords, 30000); // Every 30 seconds
      return () => clearInterval(interval); // Cleanup on unmount
    }
  }, [userGroup]);

  const handleFetchRecords = (e) => {
    e.preventDefault();
    fetchGPSRecords();
  };

  return (
    <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto' }}>
      <h2>Request GPS Records for User Group</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleFetchRecords}>
        <div style={{ marginBottom: '15px' }}>
          <label htmlFor="userGroup">User Group</label>
          <input
            type="text"
            id="userGroup"
            value={userGroup}
            onChange={(e) => setUserGroup(e.target.value)}
            placeholder="Enter user group"
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
          />
        </div>
        <button
          type="submit"
          disabled={isLoading}
          style={{
            width: '100%',
            padding: '10px',
            backgroundColor: isLoading ? '#ccc' : '#007bff',
            color: 'white',
            border: 'none',
            cursor: isLoading ? 'not-allowed' : 'pointer',
          }}
        >
          {isLoading ? 'Fetching...' : 'Fetch Records'}
        </button>
      </form>

      <h3 style={{ marginTop: '20px' }}>GPS Records</h3>
      <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '10px' }}>
        <thead>
          <tr style={{ backgroundColor: '#f2f2f2' }}>
            <th style={{ border: '1px solid #ddd', padding: '8px' }}>User</th>
            <th style={{ border: '1px solid #ddd', padding: '8px' }}>Latitude</th>
            <th style={{ border: '1px solid #ddd', padding: '8px' }}>Longitude</th>
            <th style={{ border: '1px solid #ddd', padding: '8px' }}>Timestamp</th>
            <th style={{ border: '1px solid #ddd', padding: '8px' }}>Altitude</th>
            <th style={{ border: '1px solid #ddd', padding: '8px' }}>Accuracy</th>
          </tr>
        </thead>
        <tbody>
          {gpsRecords.length > 0 ? (
            gpsRecords.map((record) => (
              <tr key={record.id}>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{record.user}</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{record.latitude}</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{record.longitude}</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                  {new Date(record.timestamp).toLocaleString()}
                </td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                  {record.altitude ?? 'N/A'}
                </td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                  {record.accuracy ?? 'N/A'}
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="6" style={{ textAlign: 'center', padding: '8px' }}>
                No records available
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default GPSReceive;