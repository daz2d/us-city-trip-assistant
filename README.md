# US City Trip Assistant

A comprehensive trip planning tool that helps you visit all major US cities at the optimal time of year, with automated flight and hotel search capabilities.

## Features

- **Auto-Location Detection** - Automatically finds your nearest airport using IP geolocation
- **15 Major US Cities** - Pre-configured with optimal visit times for NYC, LA, Chicago, San Francisco, Miami, Las Vegas, Seattle, Boston, DC, New Orleans, Austin, Nashville, Denver, Portland, and San Diego
- **Seasonal Optimization** - Each city includes best/worst months to visit based on weather and events
- **Thursday-Sunday Trips** - Automatically finds 3-4 day weekend trips (Thu-Sun)
- **Flight Search** - Real-time flight search using Amadeus API
- **4+ Star Hotels** - Finds hotels near main attractions with minimum 4-star rating
- **Central Locations** - Hotels searched near city center and major attractions
- **Annual Tour Planning** - Automatically plans visits to all cities in optimal seasons

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get API Keys

#### Amadeus API (Required for flights and hotels)
1. Sign up at https://developers.amadeus.com/
2. Create a new app to get your API Key and API Secret
3. Free tier includes 2,000 API calls/month

#### Google Maps API (Optional for enhanced location data)
1. Go to https://console.cloud.google.com/
2. Enable Maps JavaScript API and Places API
3. Create credentials to get API key

### 3. Configure Environment

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Edit `.env`:
```
AMADEUS_API_KEY=your_actual_api_key_here
AMADEUS_API_SECRET=your_actual_api_secret_here
GOOGLE_MAPS_API_KEY=your_google_api_key_here
```

## Usage

### Plan a Specific City Trip

```python
from trip_planner import TripPlanner

# Auto-detect nearest airport from your current location
planner = TripPlanner()

# Or manually specify home airport
# planner = TripPlanner(home_airport="LAX")

# Plan a trip to NYC in May 2026
trip = planner.plan_city_trip("New York City, NY", 2026, 5)

# Print summary
print(planner.get_trip_summary(trip))
```

### Plan Annual Tour of All Cities

```python
from trip_planner import TripPlanner

# Auto-detect your location
planner = TripPlanner()

# Plan visits to all cities starting January 2026
tour = planner.plan_annual_tour(2026, 1)

# Review all trips
for trip in tour['trips']:
    print(planner.get_trip_summary(trip))
```

### Search Flights Only

```python
from flight_search import FlightSearcher

searcher = FlightSearcher()

# Search LAX to JFK for Thu-Sun trip
flights = searcher.search_flights(
    origin="LAX",
    destination="JFK",
    departure_date="2026-05-14",  # Thursday
    return_date="2026-05-17",      # Sunday
    adults=1
)

# View results
if flights.get('success'):
    for offer in flights['offers'][:3]:
        print(f"${offer['price']['total']} - {offer['outbound']['stops']} stops")
```

### Search Hotels Only

```python
from hotel_search import HotelSearcher

searcher = HotelSearcher()

# Search 4+ star hotels near Times Square
hotels = searcher.search_hotels_by_geocode(
    latitude=40.7580,   # Times Square coordinates
    longitude=-73.9855,
    check_in="2026-05-14",
    check_out="2026-05-17",
    adults=1,
    min_rating=4,
    radius=2  # miles
)

# View results
if hotels.get('success'):
    for hotel in hotels['offers'][:5]:
        print(f"{hotel['name']} - {hotel['rating']} stars - ${hotel['price']['total']}")
```

### Command Line Usage

Plan a specific city:
```bash
python trip_planner.py "New York City, NY"
```

Plan annual tour:
```bash
python trip_planner.py
```

## Cities Included

| City | Airport | Best Months | Central Area |
|------|---------|-------------|--------------|
| New York City, NY | JFK/LGA/EWR | Apr, May, Sep, Oct | Midtown Manhattan |
| Los Angeles, CA | LAX | Mar-May, Sep-Nov | Downtown LA |
| Chicago, IL | ORD/MDW | May, Jun, Sep, Oct | The Loop |
| San Francisco, CA | SFO | Sep, Oct, Nov | Union Square |
| Miami, FL | MIA | Dec-Apr | Miami Beach |
| Las Vegas, NV | LAS | Mar-May, Oct-Nov | The Strip |
| Seattle, WA | SEA | Jun-Sep | Downtown Seattle |
| Boston, MA | BOS | May, Jun, Sep, Oct | Back Bay |
| Washington, DC | DCA/IAD | Apr, May, Sep, Oct | Downtown DC |
| New Orleans, LA | MSY | Feb-Apr, Oct-Nov | French Quarter |
| Austin, TX | AUS | Mar-May, Oct-Nov | Downtown Austin |
| Nashville, TN | BNA | Apr, May, Sep, Oct | Downtown Nashville |
| Denver, CO | DEN | May, Jun, Sep, Oct | Downtown Denver |
| Portland, OR | PDX | Jun-Sep | Downtown Portland |
| San Diego, CA | SAN | Apr-Jun, Sep-Oct | Gaslamp Quarter |

## Trip Requirements

- **Duration**: 3-4 days (Thursday to Sunday)
- **Hotel Rating**: Minimum 4 stars
- **Hotel Location**: Within 2 miles of city center/main attractions
- **Travelers**: Single person (1 adult)
- **Room**: Single occupancy

## Customization

### Change Home Airport

The planner auto-detects your location, but you can override it:
```python
planner = TripPlanner(home_airport="ORD")  # Force Chicago O'Hare
```

To test location detection:
```bash
python3 location_detector.py
```

### Adjust Hotel Radius

In `trip_planner.py`, modify the `plan_city_trip` method:
```python
hotels = self.hotel_searcher.search_hotels_by_geocode(
    # ... other params ...
    radius=3  # Change from 2 to 3 miles
)
```

### Add More Cities

Edit `city_data.py` and add to `MAJOR_US_CITIES` dictionary:
```python
"Phoenix, AZ": {
    "airport_code": "PHX",
    "best_months": [11, 12, 1, 2, 3],
    "main_attractions": ["Desert Botanical Garden", "Camelback Mountain"],
    "central_area": "Downtown Phoenix",
    "lat": 33.4484,
    "lon": -112.0740
}
```

## API Rate Limits

**Amadeus Test API:**
- 2,000 API calls per month (free tier)
- Each trip search uses ~2-3 calls (1 for flights, 1-2 for hotels)
- Plan accordingly: ~600-1000 trip searches per month

**Google Maps API:**
- $200 free credit per month
- Optional - only needed for enhanced location features

## Saving Results

To save trip plans to JSON:

```python
import json

trip = planner.plan_city_trip("New York City, NY", 2026, 5)

with open('nyc_trip.json', 'w') as f:
    json.dump(trip, f, indent=2)
```

## Tips

1. **Book Early**: Search 2-3 months in advance for best rates
2. **Flexible Dates**: Try different Thursdays in the optimal month
3. **Alternative Airports**: Some cities have multiple airports (NYC: JFK/LGA/EWR)
4. **Hotel Amenities**: Filter includes WiFi and parking by default
5. **Seasonal Events**: Best months often coincide with major events (check city calendars)

## Troubleshooting

### No flights found
- Check if airports are correct
- Try dates further in the future (minimum 1 week out)
- Check if API credentials are valid

### No hotels found
- Try increasing the radius parameter
- Lower minimum rating temporarily to test
- Verify check-in/check-out dates are valid

### API Authentication Error
- Verify `.env` file exists and has correct keys
- Check Amadeus dashboard for API status
- Ensure you're using test API endpoints for free tier

## Future Enhancements

- [ ] Add car rental search
- [ ] Include restaurant recommendations
- [ ] Weather forecast integration
- [ ] Budget calculator
- [ ] Export to PDF itinerary
- [ ] Multiple travelers support
- [ ] Alternative accommodations (Airbnb)
- [ ] Activity booking integration

## License

MIT License - Free to use and modify

## Support

For issues or questions, please check:
- Amadeus API Documentation: https://developers.amadeus.com/self-service
- API Status: https://developers.amadeus.com/status
