import controllers.common
import utils.gps as gps
import utils.geocode as geocode

def run():
    [lat,lon] = gps.read_coordinates()
    city = geocode.getCity(lat,lon)
    print(city)