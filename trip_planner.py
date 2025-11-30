"""
Main trip planner that combines flight and hotel searches
"""

import json
from datetime import datetime, timedelta
from calendar import monthrange
from city_data import MAJOR_US_CITIES, get_cities_by_month
from flight_search import FlightSearcher
from hotel_search import HotelSearcher
from location_detector import get_home_airport

class TripPlanner:
    def __init__(self, home_airport=None):
        """
        Initialize trip planner
        
        Args:
            home_airport: Your home airport code (optional - auto-detects if not provided)
        """
        if home_airport is None:
            self.home_airport = get_home_airport()
        else:
            self.home_airport = home_airport
        self.flight_searcher = FlightSearcher()
        self.hotel_searcher = HotelSearcher()
    
    def plan_city_trip(self, city_name, year, month, specific_thursday=None):
        """
        Plan a complete trip to a city
        
        Args:
            city_name: Name of city (e.g., "New York City, NY")
            year: Year to visit
            month: Month to visit (1-12)
            specific_thursday: Optional specific Thursday date (datetime object)
            
        Returns:
            Complete trip plan with flights and hotels
        """
        city_info = MAJOR_US_CITIES.get(city_name)
        if not city_info:
            return {"error": f"City {city_name} not found"}
        
        # Check if month is optimal
        is_optimal = month in city_info['best_months']
        is_avoid = month in city_info['avoid_months']
        
        # Find Thursdays in the month
        if specific_thursday:
            thursday = specific_thursday
            sunday = thursday + timedelta(days=3)
        else:
            thursday, sunday = self._find_best_thursday(year, month)
        
        if not thursday:
            return {"error": "No suitable Thursday found in this month"}
        
        # Search flights
        print(f"Searching flights from {self.home_airport} to {city_info['airport_code']}...")
        flights = self.flight_searcher.search_flights(
            origin=self.home_airport,
            destination=city_info['airport_code'],
            departure_date=thursday.strftime('%Y-%m-%d'),
            return_date=sunday.strftime('%Y-%m-%d'),
            adults=1
        )
        
        # Search hotels near main attractions
        print(f"Searching 4+ star hotels in {city_info['central_area']}...")
        hotels = self.hotel_searcher.search_hotels_by_geocode(
            latitude=city_info['lat'],
            longitude=city_info['lon'],
            check_in=thursday.strftime('%Y-%m-%d'),
            check_out=sunday.strftime('%Y-%m-%d'),
            adults=1,
            min_rating=4,
            radius=2
        )
        
        return {
            "city": city_name,
            "travel_dates": {
                "departure": thursday.strftime('%Y-%m-%d'),
                "return": sunday.strftime('%Y-%m-%d'),
                "duration": "3 nights, 4 days (Thu-Sun)"
            },
            "season_info": {
                "month": datetime(year, month, 1).strftime('%B'),
                "optimal": is_optimal,
                "avoid": is_avoid,
                "reason": self._get_season_reason(city_info, month)
            },
            "attractions": city_info['main_attractions'],
            "central_area": city_info['central_area'],
            "flights": flights,
            "hotels": hotels
        }
    
    def plan_annual_tour(self, start_year, start_month=None):
        """
        Plan visits to all major cities optimized by season
        
        Args:
            start_year: Year to start planning
            start_month: Month to start (default: current month)
            
        Returns:
            Complete annual tour plan
        """
        if start_month is None:
            start_month = datetime.now().month
        
        tour_plan = []
        cities_visited = set()
        
        current_month = start_month
        current_year = start_year
        
        # Plan for 12 months to cover all cities
        for _ in range(15):  # 15 months to ensure we hit all cities
            # Get cities best for this month
            month_cities = get_cities_by_month(current_month)
            
            # Filter out already visited cities
            available_cities = [c for c in month_cities if c not in cities_visited]
            
            if available_cities:
                # Pick the first available city
                city = available_cities[0]
                cities_visited.add(city)
                
                print(f"\nPlanning {city} for {datetime(current_year, current_month, 1).strftime('%B %Y')}...")
                
                trip = self.plan_city_trip(city, current_year, current_month)
                tour_plan.append(trip)
            
            # Move to next month
            current_month += 1
            if current_month > 12:
                current_month = 1
                current_year += 1
            
            # Stop if all cities visited
            if len(cities_visited) >= len(MAJOR_US_CITIES):
                break
        
        return {
            "total_cities": len(tour_plan),
            "start_date": datetime(start_year, start_month, 1).strftime('%B %Y'),
            "trips": tour_plan
        }
    
    def get_trip_summary(self, trip_plan):
        """Generate a readable summary of trip plan"""
        summary = []
        summary.append(f"\n{'='*80}")
        summary.append(f"TRIP TO {trip_plan['city'].upper()}")
        summary.append(f"{'='*80}")
        summary.append(f"\nDates: {trip_plan['travel_dates']['departure']} to {trip_plan['travel_dates']['return']}")
        summary.append(f"Duration: {trip_plan['travel_dates']['duration']}")
        
        season = trip_plan['season_info']
        summary.append(f"\nSeason: {season['month']}")
        if season['optimal']:
            summary.append(f"✓ Optimal time to visit!")
        elif season['avoid']:
            summary.append(f"⚠ Not recommended - {season['reason']}")
        else:
            summary.append(f"○ Decent time to visit")
        
        summary.append(f"\nMain Attractions:")
        for attr in trip_plan['attractions']:
            summary.append(f"  • {attr}")
        summary.append(f"\nRecommended Area: {trip_plan['central_area']}")
        
        # Flight info
        flights = trip_plan['flights']
        if flights.get('success') and flights.get('offers'):
            summary.append(f"\n--- FLIGHT OPTIONS ---")
            for i, offer in enumerate(flights['offers'][:3], 1):
                price = offer['price']
                summary.append(f"\nOption {i}: ${price['total']} {price['currency']}")
                if offer.get('outbound'):
                    outbound = offer['outbound']
                    summary.append(f"  Outbound: {outbound['departure']['time']} → {outbound['arrival']['time']}")
                    summary.append(f"  Stops: {outbound['stops']}")
        else:
            summary.append(f"\n--- FLIGHTS ---")
            summary.append(f"Error: {flights.get('error', 'No flights found')}")
        
        # Hotel info
        hotels = trip_plan['hotels']
        if hotels.get('success') and hotels.get('offers'):
            summary.append(f"\n--- HOTEL OPTIONS (4+ Stars) ---")
            for i, offer in enumerate(hotels['offers'][:5], 1):
                summary.append(f"\n{i}. {offer['name']}")
                summary.append(f"   Rating: {offer['rating']} stars")
                summary.append(f"   Price: ${offer['price']['total']} {offer['price']['currency']} total")
                if offer['price'].get('per_night'):
                    summary.append(f"   (${offer['price']['per_night']}/night)")
                summary.append(f"   Room: {offer['room']['type']}")
        else:
            summary.append(f"\n--- HOTELS ---")
            summary.append(f"Error: {hotels.get('error', 'No hotels found')}")
        
        summary.append(f"\n{'='*80}\n")
        
        return "\n".join(summary)
    
    def _find_best_thursday(self, year, month):
        """Find the best Thursday in a month (2nd or 3rd week)"""
        num_days = monthrange(year, month)[1]
        thursdays = []
        
        for day in range(1, num_days + 1):
            date = datetime(year, month, day)
            if date.weekday() == 3:  # Thursday
                thursdays.append(date)
        
        # Skip past dates
        future_thursdays = [t for t in thursdays if t >= datetime.now()]
        
        if not future_thursdays:
            return None, None
        
        # Prefer 2nd or 3rd Thursday of month
        if len(future_thursdays) >= 2:
            thursday = future_thursdays[1]  # 2nd Thursday
        else:
            thursday = future_thursdays[0]
        
        sunday = thursday + timedelta(days=3)
        return thursday, sunday
    
    def _get_season_reason(self, city_info, month):
        """Get reason for seasonal recommendation"""
        if month in city_info['best_months']:
            return "Ideal weather and events"
        elif month in city_info['avoid_months']:
            if month in [12, 1, 2, 3]:
                return "Cold weather"
            elif month in [6, 7, 8, 9]:
                return "Hot/humid or hurricane season"
            else:
                return "Not optimal season"
        else:
            return "Acceptable weather"

def main():
    """Main entry point for trip planner"""
    import sys
    import os
    
    # Check for --airport command line argument
    home_airport = None
    city_name = None
    
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] in ['--airport', '-a']:
            if i + 1 < len(args):
                home_airport = args[i + 1]
                i += 2
            else:
                print("Error: --airport requires an airport code")
                sys.exit(1)
        else:
            city_name = " ".join(args[i:])
            break
    
    # Auto-detect home airport from current location (or use specified one)
    planner = TripPlanner(home_airport=home_airport)
    
    if city_name:
        # Plan trip for specific city
        # Plan trip for next available optimal month
        for city, info in MAJOR_US_CITIES.items():
            if city.lower() == city_name.lower():
                next_month = datetime.now().month + 1
                year = datetime.now().year
                if next_month > 12:
                    next_month = 1
                    year += 1
                
                # Find next optimal month
                for month_offset in range(12):
                    test_month = (next_month + month_offset - 1) % 12 + 1
                    test_year = year if (next_month + month_offset) <= 12 else year + 1
                    
                    if test_month in info['best_months']:
                        trip = planner.plan_city_trip(city, test_year, test_month)
                        print(planner.get_trip_summary(trip))
                        break
                break
    else:
        # Plan annual tour
        print("Planning annual tour of major US cities...")
        print("This will find optimal times to visit each city.\n")
        
        tour = planner.plan_annual_tour(2026, 1)
        
        print(f"\nTotal cities planned: {tour['total_cities']}")
        print(f"Starting: {tour['start_date']}\n")
        
        for trip in tour['trips'][:3]:  # Show first 3
            print(planner.get_trip_summary(trip))

if __name__ == "__main__":
    main()
