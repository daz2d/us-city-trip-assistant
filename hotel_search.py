"""
Hotel search functionality using Amadeus API
"""

import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class HotelSearcher:
    def __init__(self):
        self.api_key = os.getenv('AMADEUS_API_KEY')
        self.api_secret = os.getenv('AMADEUS_API_SECRET')
        self.access_token = None
        self.token_expires_at = None
        
    def get_access_token(self):
        """Get OAuth access token from Amadeus"""
        from datetime import timedelta
        
        if self.access_token and self.token_expires_at and datetime.now() < self.token_expires_at:
            return self.access_token
            
        url = "https://test.api.amadeus.com/v1/security/oauth2/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret
        }
        
        try:
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            token_data = response.json()
            self.access_token = token_data['access_token']
            expires_in = token_data.get('expires_in', 1800)
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)
            return self.access_token
        except Exception as e:
            print(f"Error getting access token: {e}")
            return None
    
    def search_hotels_by_city(self, city_code, check_in, check_out, adults=1, min_rating=4):
        """
        Search for hotels in a city
        
        Args:
            city_code: IATA city code (e.g., 'NYC', 'LAX')
            check_in: Check-in date (YYYY-MM-DD)
            check_out: Check-out date (YYYY-MM-DD)
            adults: Number of adults
            min_rating: Minimum hotel rating (1-5)
            
        Returns:
            List of hotel offers
        """
        token = self.get_access_token()
        if not token:
            return {"error": "Could not authenticate with Amadeus API"}
        
        # First, get hotel list by city
        url = "https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        params = {
            "cityCode": city_code,
            "radius": 5,
            "radiusUnit": "MILE",
            "ratings": ",".join([str(i) for i in range(min_rating, 6)]),  # 4,5 for 4+ stars
            "amenities": "WIFI,PARKING",
            "hotelSource": "ALL"
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            hotels_data = response.json()
            
            hotel_ids = [h['hotelId'] for h in hotels_data.get('data', [])[:20]]  # Limit to 20 hotels
            
            if not hotel_ids:
                return {"error": "No hotels found matching criteria"}
            
            # Now get offers for these hotels
            return self.get_hotel_offers(hotel_ids, check_in, check_out, adults)
            
        except Exception as e:
            return {"error": f"Error searching hotels: {str(e)}"}
    
    def search_hotels_by_geocode(self, latitude, longitude, check_in, check_out, adults=1, min_rating=4, radius=2):
        """
        Search for hotels by geographic coordinates (better for central locations)
        
        Args:
            latitude: Latitude of center point
            longitude: Longitude of center point
            check_in: Check-in date (YYYY-MM-DD)
            check_out: Check-out date (YYYY-MM-DD)
            adults: Number of adults
            min_rating: Minimum hotel rating (1-5)
            radius: Search radius in miles
            
        Returns:
            List of hotel offers
        """
        token = self.get_access_token()
        if not token:
            return {"error": "Could not authenticate with Amadeus API"}
        
        url = "https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-geocode"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "radius": radius,
            "radiusUnit": "MILE",
            "ratings": ",".join([str(i) for i in range(min_rating, 6)]),
            "hotelSource": "ALL"
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            hotels_data = response.json()
            
            hotel_ids = [h['hotelId'] for h in hotels_data.get('data', [])[:20]]
            
            if not hotel_ids:
                return {"error": "No hotels found matching criteria"}
            
            return self.get_hotel_offers(hotel_ids, check_in, check_out, adults)
            
        except Exception as e:
            return {"error": f"Error searching hotels: {str(e)}"}
    
    def get_hotel_offers(self, hotel_ids, check_in, check_out, adults=1):
        """
        Get offers for specific hotels
        
        Args:
            hotel_ids: List of hotel IDs
            check_in: Check-in date (YYYY-MM-DD)
            check_out: Check-out date (YYYY-MM-DD)
            adults: Number of adults
            
        Returns:
            Hotel offers with pricing
        """
        token = self.get_access_token()
        if not token:
            return {"error": "Could not authenticate"}
        
        url = "https://test.api.amadeus.com/v3/shopping/hotel-offers"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        params = {
            "hotelIds": ",".join(hotel_ids),
            "checkInDate": check_in,
            "checkOutDate": check_out,
            "adults": adults,
            "roomQuantity": 1,
            "currency": "USD",
            "bestRateOnly": "true"
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            offers = []
            for hotel in data.get('data', []):
                hotel_info = self._parse_hotel_offer(hotel)
                if hotel_info:
                    offers.append(hotel_info)
            
            # Sort by price
            offers.sort(key=lambda x: x.get('price', {}).get('total', float('inf')))
            
            return {
                "success": True,
                "check_in": check_in,
                "check_out": check_out,
                "offers": offers
            }
            
        except Exception as e:
            return {"error": f"Error getting hotel offers: {str(e)}"}
    
    def _parse_hotel_offer(self, hotel_data):
        """Parse hotel offer data"""
        try:
            hotel = hotel_data.get('hotel', {})
            offers = hotel_data.get('offers', [])
            
            if not offers:
                return None
            
            best_offer = offers[0]  # Already filtered for best rate
            
            price = best_offer.get('price', {})
            room = best_offer.get('room', {})
            
            return {
                "hotel_id": hotel.get('hotelId', ''),
                "name": hotel.get('name', 'Unknown Hotel'),
                "rating": hotel.get('rating', 'N/A'),
                "address": hotel.get('address', {}),
                "contact": hotel.get('contact', {}),
                "price": {
                    "total": float(price.get('total', 0)),
                    "currency": price.get('currency', 'USD'),
                    "per_night": float(price.get('base', 0)) if price.get('base') else None
                },
                "room": {
                    "type": room.get('typeEstimated', {}).get('category', 'Standard'),
                    "beds": room.get('typeEstimated', {}).get('beds', 'Unknown'),
                    "description": room.get('description', {}).get('text', '')
                },
                "amenities": hotel_data.get('amenities', []),
                "cancellation": best_offer.get('policies', {}).get('cancellation', {})
            }
        except Exception as e:
            print(f"Error parsing hotel: {e}")
            return None

def main():
    """Test hotel search functionality"""
    searcher = HotelSearcher()
    
    # Example: Search for hotels in NYC by coordinates (near Times Square)
    result = searcher.search_hotels_by_geocode(
        latitude=40.7580,
        longitude=-73.9855,
        check_in="2026-05-14",
        check_out="2026-05-17",
        adults=1,
        min_rating=4,
        radius=2
    )
    
    if result.get('success'):
        print(f"\nFound {len(result['offers'])} hotel offers:")
        for i, offer in enumerate(result['offers'][:3], 1):
            print(f"\n--- Hotel {i} ---")
            print(f"Name: {offer['name']}")
            print(f"Rating: {offer['rating']} stars")
            print(f"Price: ${offer['price']['total']} {offer['price']['currency']}")
            print(f"Room: {offer['room']['type']}")
    else:
        print(f"Error: {result.get('error')}")

if __name__ == "__main__":
    main()
