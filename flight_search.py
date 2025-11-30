"""
Flight search functionality using Amadeus API
"""

import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class FlightSearcher:
    def __init__(self):
        self.api_key = os.getenv('AMADEUS_API_KEY')
        self.api_secret = os.getenv('AMADEUS_API_SECRET')
        self.access_token = None
        self.token_expires_at = None
        
    def get_access_token(self):
        """Get OAuth access token from Amadeus"""
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
            # Token expires in seconds, convert to datetime
            expires_in = token_data.get('expires_in', 1800)
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)
            return self.access_token
        except Exception as e:
            print(f"Error getting access token: {e}")
            return None
    
    def search_flights(self, origin, destination, departure_date, return_date=None, adults=1):
        """
        Search for flights
        
        Args:
            origin: Origin airport code (e.g., 'LAX')
            destination: Destination airport code (e.g., 'JFK')
            departure_date: Departure date in YYYY-MM-DD format
            return_date: Return date in YYYY-MM-DD format (optional for round trip)
            adults: Number of adult passengers
            
        Returns:
            List of flight offers
        """
        token = self.get_access_token()
        if not token:
            return {"error": "Could not authenticate with Amadeus API"}
        
        url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        params = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": departure_date,
            "adults": adults,
            "currencyCode": "USD",
            "max": 10  # Limit results
        }
        
        if return_date:
            params["returnDate"] = return_date
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Parse and format flight offers
            offers = []
            for offer in data.get('data', []):
                flight_info = self._parse_flight_offer(offer)
                offers.append(flight_info)
            
            return {
                "success": True,
                "origin": origin,
                "destination": destination,
                "departure_date": departure_date,
                "return_date": return_date,
                "offers": offers
            }
        except Exception as e:
            return {"error": f"Error searching flights: {str(e)}"}
    
    def _parse_flight_offer(self, offer):
        """Parse flight offer data into readable format"""
        try:
            price = offer.get('price', {})
            itineraries = offer.get('itineraries', [])
            
            outbound = itineraries[0] if len(itineraries) > 0 else {}
            return_flight = itineraries[1] if len(itineraries) > 1 else None
            
            return {
                "price": {
                    "total": float(price.get('total', 0)),
                    "currency": price.get('currency', 'USD')
                },
                "outbound": self._parse_itinerary(outbound),
                "return": self._parse_itinerary(return_flight) if return_flight else None,
                "booking_link": offer.get('self', {}).get('href', ''),
                "seats_available": offer.get('numberOfBookableSeats', 'Unknown')
            }
        except Exception as e:
            return {"error": f"Error parsing offer: {str(e)}"}
    
    def _parse_itinerary(self, itinerary):
        """Parse itinerary segment"""
        if not itinerary:
            return None
            
        segments = itinerary.get('segments', [])
        if not segments:
            return None
        
        first_segment = segments[0]
        last_segment = segments[-1]
        
        departure = first_segment.get('departure', {})
        arrival = last_segment.get('arrival', {})
        
        return {
            "departure": {
                "airport": departure.get('iataCode', ''),
                "time": departure.get('at', '')
            },
            "arrival": {
                "airport": arrival.get('iataCode', ''),
                "time": arrival.get('at', '')
            },
            "duration": itinerary.get('duration', ''),
            "stops": len(segments) - 1,
            "carriers": [seg.get('carrierCode', '') for seg in segments]
        }

    def find_best_thursday_to_sunday(self, origin, destination, year, month):
        """
        Find the best Thu-Sun trip in a given month
        
        Args:
            origin: Origin airport code
            destination: Destination airport code
            year: Year
            month: Month (1-12)
            
        Returns:
            Best flight option for Thu-Sun trip
        """
        from calendar import monthrange
        
        # Get all Thursdays in the month
        num_days = monthrange(year, month)[1]
        thursdays = []
        
        for day in range(1, num_days + 1):
            date = datetime(year, month, day)
            if date.weekday() == 3:  # Thursday is 3
                thursdays.append(date)
        
        best_offer = None
        best_price = float('inf')
        
        for thursday in thursdays:
            # Skip if date is in the past
            if thursday < datetime.now():
                continue
                
            sunday = thursday + timedelta(days=3)
            
            # Format dates
            dep_date = thursday.strftime('%Y-%m-%d')
            ret_date = sunday.strftime('%Y-%m-%d')
            
            # Search flights
            result = self.search_flights(origin, destination, dep_date, ret_date)
            
            if result.get('success') and result.get('offers'):
                for offer in result['offers']:
                    price = offer.get('price', {}).get('total', float('inf'))
                    if price < best_price:
                        best_price = price
                        best_offer = {
                            **offer,
                            "departure_date": dep_date,
                            "return_date": ret_date
                        }
        
        return best_offer

def main():
    """Test flight search functionality"""
    searcher = FlightSearcher()
    
    # Example: Search for flights from LAX to JFK
    result = searcher.search_flights(
        origin="LAX",
        destination="JFK",
        departure_date="2026-05-14",
        return_date="2026-05-17",
        adults=1
    )
    
    if result.get('success'):
        print(f"\nFound {len(result['offers'])} flight offers:")
        for i, offer in enumerate(result['offers'][:3], 1):
            print(f"\n--- Offer {i} ---")
            print(f"Price: ${offer['price']['total']} {offer['price']['currency']}")
            if offer.get('outbound'):
                print(f"Outbound: {offer['outbound']['departure']['airport']} → {offer['outbound']['arrival']['airport']}")
                print(f"  Departure: {offer['outbound']['departure']['time']}")
                print(f"  Stops: {offer['outbound']['stops']}")
    else:
        print(f"Error: {result.get('error')}")

if __name__ == "__main__":
    main()
