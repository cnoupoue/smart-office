from geopy.geocoders import Nominatim

def get_address(latitude, longitude):
    # Initialize geolocator
    geoLoc = Nominatim(user_agent="GeoLoc")

    # Perform reverse geocoding
    location = geoLoc.reverse((latitude, longitude), language='en', exactly_one=True)

    if location:
        # Get raw address data as a dictionary
        address = location.raw.get('address', {})
        # print("Raw Address Data:", address)
        
        # Extract the smallest accepted locality, including tower and city
        # smallest_city = (
        #     address.get('municipality') or  # Municipality
        #     address.get('city') or          # City
        #     address.get('county') or        # County
        #     address.get('state')            # Finally, fallback to state
        # )
        
        # road = address.get('road')

        return address
    else:
        return None
