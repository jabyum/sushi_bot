import requests
api_key = "f3690a3e-fec7-477f-9c4b-3a75a0c23530"
def geolocators(latitude, longitude):
    url = f"https://geocode-maps.yandex.ru/1.x/?apikey={api_key}&geocode={longitude},{latitude}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        address = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
        return address
    else:
        return f'Не удалось расшифровать адрес по координатам {latitude, longitude}'

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