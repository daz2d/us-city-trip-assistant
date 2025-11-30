"""
Major US cities with optimal visit times and main attractions
"""

MAJOR_US_CITIES = {
    "New York City, NY": {
        "airport_code": "JFK",
        "alt_airports": ["LGA", "EWR"],
        "best_months": [4, 5, 9, 10],  # Apr, May, Sep, Oct
        "avoid_months": [1, 2, 7, 8],  # Too cold or too hot/humid
        "main_attractions": [
            "Times Square",
            "Central Park",
            "Empire State Building",
            "Statue of Liberty",
            "Metropolitan Museum of Art"
        ],
        "central_area": "Midtown Manhattan",
        "lat": 40.7128,
        "lon": -74.0060
    },
    "Los Angeles, CA": {
        "airport_code": "LAX",
        "alt_airports": ["BUR", "SNA"],
        "best_months": [3, 4, 5, 9, 10, 11],  # Spring and Fall
        "avoid_months": [],
        "main_attractions": [
            "Hollywood Walk of Fame",
            "Griffith Observatory",
            "Santa Monica Pier",
            "Getty Center",
            "Universal Studios"
        ],
        "central_area": "Downtown LA",
        "lat": 34.0522,
        "lon": -118.2437
    },
    "Chicago, IL": {
        "airport_code": "ORD",
        "alt_airports": ["MDW"],
        "best_months": [5, 6, 9, 10],  # Late spring and early fall
        "avoid_months": [12, 1, 2],  # Too cold
        "main_attractions": [
            "Millennium Park",
            "Navy Pier",
            "Art Institute of Chicago",
            "Willis Tower",
            "Magnificent Mile"
        ],
        "central_area": "The Loop",
        "lat": 41.8781,
        "lon": -87.6298
    },
    "San Francisco, CA": {
        "airport_code": "SFO",
        "alt_airports": ["OAK", "SJC"],
        "best_months": [9, 10, 11],  # Fall (warmest months)
        "avoid_months": [6, 7, 8],  # Foggy summer
        "main_attractions": [
            "Golden Gate Bridge",
            "Fisherman's Wharf",
            "Alcatraz Island",
            "Cable Cars",
            "Chinatown"
        ],
        "central_area": "Union Square",
        "lat": 37.7749,
        "lon": -122.4194
    },
    "Miami, FL": {
        "airport_code": "MIA",
        "alt_airports": ["FLL"],
        "best_months": [12, 1, 2, 3, 4],  # Winter (dry season)
        "avoid_months": [6, 7, 8, 9],  # Hurricane season
        "main_attractions": [
            "South Beach",
            "Art Deco Historic District",
            "Vizcaya Museum",
            "Wynwood Walls",
            "Bayside Marketplace"
        ],
        "central_area": "Miami Beach",
        "lat": 25.7617,
        "lon": -80.1918
    },
    "Las Vegas, NV": {
        "airport_code": "LAS",
        "alt_airports": [],
        "best_months": [3, 4, 5, 10, 11],  # Spring and fall
        "avoid_months": [7, 8],  # Extreme heat
        "main_attractions": [
            "The Strip",
            "Fremont Street",
            "Bellagio Fountains",
            "High Roller Observation Wheel",
            "Red Rock Canyon"
        ],
        "central_area": "The Strip",
        "lat": 36.1699,
        "lon": -115.1398
    },
    "Seattle, WA": {
        "airport_code": "SEA",
        "alt_airports": [],
        "best_months": [6, 7, 8, 9],  # Summer (dry season)
        "avoid_months": [11, 12, 1],  # Rainy season
        "main_attractions": [
            "Pike Place Market",
            "Space Needle",
            "Chihuly Garden and Glass",
            "Seattle Waterfront",
            "Museum of Pop Culture"
        ],
        "central_area": "Downtown Seattle",
        "lat": 47.6062,
        "lon": -122.3321
    },
    "Boston, MA": {
        "airport_code": "BOS",
        "alt_airports": [],
        "best_months": [5, 6, 9, 10],  # Late spring and fall
        "avoid_months": [1, 2, 3],  # Cold winter
        "main_attractions": [
            "Freedom Trail",
            "Fenway Park",
            "Boston Common",
            "Museum of Fine Arts",
            "New England Aquarium"
        ],
        "central_area": "Back Bay",
        "lat": 42.3601,
        "lon": -71.0589
    },
    "Washington, DC": {
        "airport_code": "DCA",
        "alt_airports": ["IAD", "BWI"],
        "best_months": [4, 5, 9, 10],  # Cherry blossoms in spring
        "avoid_months": [7, 8],  # Hot and humid
        "main_attractions": [
            "National Mall",
            "Smithsonian Museums",
            "White House",
            "Lincoln Memorial",
            "US Capitol"
        ],
        "central_area": "Downtown DC",
        "lat": 38.9072,
        "lon": -77.0369
    },
    "New Orleans, LA": {
        "airport_code": "MSY",
        "alt_airports": [],
        "best_months": [2, 3, 4, 10, 11],  # Mardi Gras season, fall
        "avoid_months": [6, 7, 8, 9],  # Hot, humid, hurricanes
        "main_attractions": [
            "French Quarter",
            "Bourbon Street",
            "Jackson Square",
            "Garden District",
            "St. Louis Cathedral"
        ],
        "central_area": "French Quarter",
        "lat": 29.9511,
        "lon": -90.0715
    },
    "Austin, TX": {
        "airport_code": "AUS",
        "alt_airports": [],
        "best_months": [3, 4, 5, 10, 11],  # Spring and fall
        "avoid_months": [7, 8],  # Extreme heat
        "main_attractions": [
            "6th Street",
            "Texas State Capitol",
            "Lady Bird Lake",
            "South Congress",
            "Zilker Park"
        ],
        "central_area": "Downtown Austin",
        "lat": 30.2672,
        "lon": -97.7431
    },
    "Nashville, TN": {
        "airport_code": "BNA",
        "alt_airports": [],
        "best_months": [4, 5, 9, 10],  # Spring and fall
        "avoid_months": [7, 8],  # Hot and humid
        "main_attractions": [
            "Broadway",
            "Country Music Hall of Fame",
            "Ryman Auditorium",
            "Grand Ole Opry",
            "Parthenon"
        ],
        "central_area": "Downtown Nashville",
        "lat": 36.1627,
        "lon": -86.7816
    },
    "Denver, CO": {
        "airport_code": "DEN",
        "alt_airports": [],
        "best_months": [5, 6, 9, 10],  # Spring and fall
        "avoid_months": [12, 1, 2],  # Cold winter
        "main_attractions": [
            "Red Rocks Park",
            "16th Street Mall",
            "Denver Art Museum",
            "Larimer Square",
            "Union Station"
        ],
        "central_area": "Downtown Denver",
        "lat": 39.7392,
        "lon": -104.9903
    },
    "Portland, OR": {
        "airport_code": "PDX",
        "alt_airports": [],
        "best_months": [6, 7, 8, 9],  # Summer (dry season)
        "avoid_months": [11, 12, 1],  # Rainy season
        "main_attractions": [
            "Powell's City of Books",
            "Washington Park",
            "Portland Japanese Garden",
            "Food Carts",
            "Pittock Mansion"
        ],
        "central_area": "Downtown Portland",
        "lat": 45.5152,
        "lon": -122.6784
    },
    "San Diego, CA": {
        "airport_code": "SAN",
        "alt_airports": [],
        "best_months": [4, 5, 6, 9, 10],  # Spring and fall
        "avoid_months": [],  # Great year-round
        "main_attractions": [
            "Balboa Park",
            "San Diego Zoo",
            "USS Midway Museum",
            "Gaslamp Quarter",
            "La Jolla Cove"
        ],
        "central_area": "Gaslamp Quarter",
        "lat": 32.7157,
        "lon": -117.1611
    },
    "Atlanta, GA": {
        "airport_code": "ATL",
        "alt_airports": [],
        "best_months": [3, 4, 5, 9, 10, 11],  # Spring and fall
        "avoid_months": [7, 8],  # Hot and humid
        "main_attractions": [
            "Georgia Aquarium",
            "World of Coca-Cola",
            "Martin Luther King Jr. National Historical Park",
            "Piedmont Park",
            "Fox Theatre"
        ],
        "central_area": "Downtown Atlanta",
        "lat": 33.7490,
        "lon": -84.3880
    },
    "Memphis, TN": {
        "airport_code": "MEM",
        "alt_airports": [],
        "best_months": [4, 5, 9, 10],  # Spring and fall
        "avoid_months": [7, 8],  # Hot and humid
        "main_attractions": [
            "Beale Street",
            "Graceland",
            "National Civil Rights Museum",
            "Sun Studio",
            "Memphis Zoo"
        ],
        "central_area": "Downtown Memphis",
        "lat": 35.1495,
        "lon": -90.0490
    }
}

def get_city_info(city_name):
    """Get information about a specific city"""
    return MAJOR_US_CITIES.get(city_name)

def get_all_cities():
    """Get list of all major cities"""
    return list(MAJOR_US_CITIES.keys())

def get_cities_by_month(month):
    """Get cities that are best to visit in a given month"""
    cities = []
    for city, info in MAJOR_US_CITIES.items():
        if month in info['best_months']:
            cities.append(city)
    return cities
