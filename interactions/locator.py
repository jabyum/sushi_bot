import requests

def geolocators(latitude, longitude):
    url = f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json&addressdetails=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        address = data['display_name']
        return address
    else:
        return None

# from geopy.geocoders import Nominatim
# from geopy.exc import GeocoderUnavailable
# import ssl
#
# ctx = ssl.create_default_context()
# ctx.check_hostname = False
# ctx.verify_mode = ssl.CERT_NONE
#
# def geolocators(latitude, longitude):
#     geolocator = Nominatim(user_agent="geo_locator", ssl_context=ctx)
#     try:
#         location = geolocator.reverse((latitude, longitude), language='ru')
#         return location.address
#     except GeocoderUnavailable as e:
#         print("Ошибка:", e)
#         return None