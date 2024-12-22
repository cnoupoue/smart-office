from geopy.geocoders import Nominatim

def getCity(latitude, longitude):
    # Initialize geolocator
    geoLoc = Nominatim(user_agent="GeoLoc")

    # Perform reverse geocoding
    location = geoLoc.reverse((latitude, longitude), language='en', exactly_one=True)

    if location:
        # Get raw address data as a dictionary
        address = location.raw.get('address', {})
        # print("Raw Address Data:", address)
        
        # Extract the smallest accepted locality, including tower and city
        smallest_city = (
            address.get('municipality') or  # Municipality
            address.get('city') or          # City
            address.get('county') or        # County
            address.get('state')            # Finally, fallback to state
        )
        
        return smallest_city
    else:
        return None