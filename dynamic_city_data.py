"""
Dynamic city data fetcher using free APIs
"""

import requests
import json
import os
from datetime import datetime

class CityDataFetcher:
    def __init__(self):
        self.cache_file = "city_cache.json"
        self.cache_duration = 30 * 24 * 60 * 60  # 30 days in seconds
        
    def get_us_cities_by_population(self, min_population=500000):
        """
        Fetch major US cities from GeoNames API (free, no key needed)
        
        Args:
            min_population: Minimum population to consider
            
        Returns:
            List of city data
        """
        cities = []
        
        # Use GeoNames free API - no key required for basic searches
        url = "http://api.geonames.org/searchJSON"
        
        # Search for major US cities
        params = {
            "country": "US",
            "featureClass": "P",  # Populated places
            "maxRows": 100,
            "username": "demo",  # Free demo account
            "orderby": "population",
            "cities": "cities15000"  # Cities with population > 15,000
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            for place in data.get('geonames', []):
                population = place.get('population', 0)
                if population >= min_population:
                    cities.append({
                        "name": place.get('name', ''),
                        "state": place.get('adminCode1', ''),
                        "lat": float(place.get('lat', 0)),
                        "lon": float(place.get('lng', 0)),
                        "population": population
                    })
        except Exception as e:
            print(f"Error fetching cities from GeoNames: {e}")
        
        return cities
    
    def find_nearest_airport_code(self, lat, lon):
        """
        Find nearest airport using free airport API
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Airport code (IATA)
        """
        # Use aviationstack free API or fallback to local lookup
        from location_detector import find_nearest_airport, US_AIRPORTS
        
        # Find from our known airports
        code, info, distance = find_nearest_airport(lat, lon)
        return code
    
    def get_city_attractions_wikipedia(self, city_name, state):
        """
        Get attractions from Wikipedia API (free, no key needed)
        
        Args:
            city_name: Name of city
            state: State abbreviation
            
        Returns:
            List of attractions
        """
        attractions = []
        
        try:
            # Use Wikipedia API to get city page
            url = "https://en.wikipedia.org/w/api.php"
            params = {
                "action": "query",
                "format": "json",
                "titles": f"{city_name}",
                "prop": "extracts",
                "exintro": True,
                "explaintext": True
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            # Parse for common attraction keywords
            pages = data.get('query', {}).get('pages', {})
            for page_id, page in pages.items():
                extract = page.get('extract', '')
                # Simple extraction - look for common patterns
                # This is basic; ideally you'd use NLP
                if 'museum' in extract.lower() or 'park' in extract.lower():
                    # Placeholder - would need more sophisticated parsing
                    pass
        except Exception as e:
            pass
        
        # Return default attractions for now
        return self._get_default_attractions(city_name)
    
    def _get_default_attractions(self, city_name):
        """Fallback to common US city attractions"""
        common = {
            "downtown": f"Downtown {city_name}",
            "museum": f"{city_name} Museum of Art",
            "park": f"City Park",
            "historic": f"Historic District",
            "waterfront": "Waterfront"
        }
        return list(common.values())[:5]
    
    def get_best_months_by_latitude(self, lat):
        """
        Determine best visit months based on latitude/climate
        
        Args:
            lat: Latitude
            
        Returns:
            tuple: (best_months, avoid_months)
        """
        # Simple climate-based heuristics
        if lat > 45:  # Northern cities (e.g., Seattle)
            return ([6, 7, 8, 9], [11, 12, 1, 2])
        elif lat > 40:  # Mid-latitude (e.g., NYC, Chicago)
            return ([4, 5, 9, 10], [12, 1, 2])
        elif lat > 35:  # Southern temperate (e.g., LA, Atlanta)
            return ([3, 4, 5, 9, 10, 11], [7, 8])
        else:  # Southern/tropical (e.g., Miami)
            return ([11, 12, 1, 2, 3, 4], [6, 7, 8, 9])
    
    def build_city_data(self, city_name, state_abbr=None):
        """
        Dynamically build city data structure
        
        Args:
            city_name: City name
            state_abbr: State abbreviation (optional)
            
        Returns:
            dict: City data structure
        """
        # Try to find city
        query = f"{city_name}, {state_abbr}" if state_abbr else city_name
        
        # Use Nominatim (OpenStreetMap) - free geocoding
        try:
            geocode_url = "https://nominatim.openstreetmap.org/search"
            params = {
                "q": query,
                "country": "United States",
                "format": "json",
                "limit": 1
            }
            headers = {
                "User-Agent": "USCityTripAssistant/1.0"
            }
            
            response = requests.get(geocode_url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                return None
            
            result = data[0]
            lat = float(result['lat'])
            lon = float(result['lon'])
            display_name = result.get('display_name', '')
            
            # Extract state from display_name
            parts = display_name.split(',')
            state = parts[-2].strip() if len(parts) >= 2 else state_abbr or "Unknown"
            
            # Find nearest airport
            airport_code = self.find_nearest_airport_code(lat, lon)
            
            # Get best months based on latitude
            best_months, avoid_months = self.get_best_months_by_latitude(lat)
            
            # Get attractions (would be enhanced with real API)
            attractions = self._get_default_attractions(city_name)
            
            city_data = {
                "airport_code": airport_code,
                "alt_airports": [],
                "best_months": best_months,
                "avoid_months": avoid_months,
                "main_attractions": attractions,
                "central_area": f"Downtown {city_name}",
                "lat": lat,
                "lon": lon,
                "population": result.get('importance', 0) * 1000000  # Rough estimate
            }
            
            return city_data
            
        except Exception as e:
            print(f"Error fetching city data for {query}: {e}")
            return None
    
    def get_or_fetch_city(self, city_name, state_abbr=None):
        """
        Get city data from cache or fetch dynamically
        
        Args:
            city_name: City name
            state_abbr: State abbreviation
            
        Returns:
            dict: City data
        """
        # Load cache
        cache = self._load_cache()
        
        cache_key = f"{city_name}, {state_abbr}" if state_abbr else city_name
        
        # Check if in cache and not expired
        if cache_key in cache:
            cached_data = cache[cache_key]
            if datetime.now().timestamp() - cached_data.get('cached_at', 0) < self.cache_duration:
                return cached_data['data']
        
        # Fetch new data
        print(f"🔍 Fetching data for {cache_key}...")
        city_data = self.build_city_data(city_name, state_abbr)
        
        if city_data:
            # Save to cache
            cache[cache_key] = {
                'data': city_data,
                'cached_at': datetime.now().timestamp()
            }
            self._save_cache(cache)
        
        return city_data
    
    def _load_cache(self):
        """Load city cache from file"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _save_cache(self, cache):
        """Save city cache to file"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(cache, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save cache: {e}")

def main():
    """Test dynamic city fetching"""
    fetcher = CityDataFetcher()
    
    test_cities = [
        ("Atlanta", "GA"),
        ("Memphis", "TN"),
        ("Phoenix", "AZ"),
        ("Philadelphia", "PA")
    ]
    
    for city, state in test_cities:
        print(f"\n{'='*60}")
        print(f"Testing: {city}, {state}")
        print('='*60)
        
        data = fetcher.get_or_fetch_city(city, state)
        
        if data:
            print(f"✅ Found!")
            print(f"  Airport: {data['airport_code']}")
            print(f"  Location: {data['lat']}, {data['lon']}")
            print(f"  Best months: {data['best_months']}")
            print(f"  Attractions: {', '.join(data['main_attractions'][:3])}")
        else:
            print(f"❌ Not found")

if __name__ == "__main__":
    main()
