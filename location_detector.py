"""
Detect current location and find nearest airport
"""

import requests
import json
from math import radians, cos, sin, asin, sqrt

# Major US airports with coordinates
US_AIRPORTS = {
    "JFK": {"name": "New York JFK", "lat": 40.6413, "lon": -73.7781, "city": "New York, NY"},
    "LAX": {"name": "Los Angeles", "lat": 33.9416, "lon": -118.4085, "city": "Los Angeles, CA"},
    "ORD": {"name": "Chicago O'Hare", "lat": 41.9742, "lon": -87.9073, "city": "Chicago, IL"},
    "DFW": {"name": "Dallas/Fort Worth", "lat": 32.8998, "lon": -97.0403, "city": "Dallas, TX"},
    "DEN": {"name": "Denver", "lat": 39.8561, "lon": -104.6737, "city": "Denver, CO"},
    "ATL": {"name": "Atlanta", "lat": 33.6407, "lon": -84.4277, "city": "Atlanta, GA"},
    "SFO": {"name": "San Francisco", "lat": 37.6213, "lon": -122.3790, "city": "San Francisco, CA"},
    "SEA": {"name": "Seattle-Tacoma", "lat": 47.4502, "lon": -122.3088, "city": "Seattle, WA"},
    "LAS": {"name": "Las Vegas", "lat": 36.0840, "lon": -115.1537, "city": "Las Vegas, NV"},
    "MCO": {"name": "Orlando", "lat": 28.4312, "lon": -81.3081, "city": "Orlando, FL"},
    "MIA": {"name": "Miami", "lat": 25.7959, "lon": -80.2870, "city": "Miami, FL"},
    "PHX": {"name": "Phoenix", "lat": 33.4352, "lon": -112.0101, "city": "Phoenix, AZ"},
    "BOS": {"name": "Boston Logan", "lat": 42.3656, "lon": -71.0096, "city": "Boston, MA"},
    "IAH": {"name": "Houston", "lat": 29.9902, "lon": -95.3368, "city": "Houston, TX"},
    "DCA": {"name": "Washington Reagan", "lat": 38.8512, "lon": -77.0402, "city": "Washington, DC"},
    "EWR": {"name": "Newark", "lat": 40.6895, "lon": -74.1745, "city": "Newark, NJ"},
    "MSY": {"name": "New Orleans", "lat": 29.9902, "lon": -90.2580, "city": "New Orleans, LA"},
    "DTW": {"name": "Detroit", "lat": 42.2162, "lon": -83.3554, "city": "Detroit, MI"},
    "PHL": {"name": "Philadelphia", "lat": 39.8744, "lon": -75.2424, "city": "Philadelphia, PA"},
    "LGA": {"name": "New York LaGuardia", "lat": 40.7769, "lon": -73.8740, "city": "New York, NY"},
    "MDW": {"name": "Chicago Midway", "lat": 41.7868, "lon": -87.7522, "city": "Chicago, IL"},
    "SAN": {"name": "San Diego", "lat": 32.7338, "lon": -117.1933, "city": "San Diego, CA"},
    "PDX": {"name": "Portland", "lat": 45.5898, "lon": -122.5951, "city": "Portland, OR"},
    "BNA": {"name": "Nashville", "lat": 36.1245, "lon": -86.6782, "city": "Nashville, TN"},
    "AUS": {"name": "Austin", "lat": 30.1945, "lon": -97.6699, "city": "Austin, TX"},
}

def get_current_location():
    """
    Get current location using IP-based geolocation (free, no API key needed)
    
    Returns:
        dict: Location data with latitude, longitude, city, region, country
    """
    try:
        # Use ipapi.co - free IP geolocation service (no API key required)
        response = requests.get('https://ipapi.co/json/', timeout=5)
        response.raise_for_status()
        data = response.json()
        
        return {
            "latitude": float(data.get('latitude', 0)),
            "longitude": float(data.get('longitude', 0)),
            "city": data.get('city', 'Unknown'),
            "region": data.get('region', 'Unknown'),
            "country": data.get('country_name', 'Unknown'),
            "ip": data.get('ip', 'Unknown')
        }
    except Exception as e:
        print(f"Error detecting location: {e}")
        print("Using default location: Los Angeles, CA")
        return {
            "latitude": 34.0522,
            "longitude": -118.2437,
            "city": "Los Angeles",
            "region": "California",
            "country": "United States"
        }

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points on Earth
    
    Args:
        lat1, lon1: Coordinates of first point
        lat2, lon2: Coordinates of second point
        
    Returns:
        float: Distance in miles
    """
    # Convert to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in miles
    r = 3956
    
    return c * r

def find_nearest_airport(latitude, longitude):
    """
    Find the nearest major US airport to given coordinates
    
    Args:
        latitude: Latitude of location
        longitude: Longitude of location
        
    Returns:
        tuple: (airport_code, airport_info, distance_miles)
    """
    nearest_airport = None
    nearest_distance = float('inf')
    nearest_code = None
    
    for code, airport in US_AIRPORTS.items():
        distance = haversine_distance(
            latitude, longitude,
            airport['lat'], airport['lon']
        )
        
        if distance < nearest_distance:
            nearest_distance = distance
            nearest_airport = airport
            nearest_code = code
    
    return nearest_code, nearest_airport, nearest_distance

def get_home_airport():
    """
    Detect current location and return nearest airport code
    
    Returns:
        str: Airport code (e.g., "LAX")
    """
    location = get_current_location()
    
    print(f"\n📍 Detected location: {location['city']}, {location['region']}")
    
    airport_code, airport_info, distance = find_nearest_airport(
        location['latitude'],
        location['longitude']
    )
    
    print(f"✈️  Nearest airport: {airport_info['name']} ({airport_code})")
    print(f"📏 Distance: {distance:.1f} miles\n")
    
    return airport_code

def main():
    """Test location detection"""
    location = get_current_location()
    print("\n" + "="*60)
    print("LOCATION DETECTION")
    print("="*60)
    print(f"\nYour Location:")
    print(f"  IP: {location.get('ip', 'Unknown')}")
    print(f"  City: {location['city']}")
    print(f"  Region: {location['region']}")
    print(f"  Country: {location['country']}")
    print(f"  Coordinates: {location['latitude']}, {location['longitude']}")
    
    airport_code, airport_info, distance = find_nearest_airport(
        location['latitude'],
        location['longitude']
    )
    
    print(f"\nNearest Airport:")
    print(f"  Code: {airport_code}")
    print(f"  Name: {airport_info['name']}")
    print(f"  City: {airport_info['city']}")
    print(f"  Distance: {distance:.1f} miles")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
