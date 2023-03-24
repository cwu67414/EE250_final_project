import requests
import datetime
import time

# OpenWeatherMap API: https://openweathermap.org/current

# TODO: Sign up for an API key
OWM_API_KEY = 'a6868ed07eeb6ee1046d83ef083635f0'  # OpenWeatherMap API Key


def get_weather(user_zip):
    params = {
        'appid': OWM_API_KEY,
        # TODO: referencing the API documentation, add the missing parameters for zip code and units (Fahrenheit)
        'zip': user_zip,
        'units': 'imperial'
    }
    
    response = requests.get('http://api.openweathermap.org/data/2.5/weather', params)

    if response.status_code == 200: # Status: OK
        data = response.json()

        # TODO: Extract the weather from data, and return as a tuple
        data_temp = data["main"]["temp"]
        data_cloud = data["clouds"]["all"]
        data_unixsunrise = data["sys"]["sunrise"]
        data_unixsunset = data["sys"]["sunset"]
        normal_sunrise = datetime.datetime.fromtimestamp(data_unixsunrise).strftime('%H:%M:%S')
        normal_sunset = datetime.datetime.fromtimestamp(data_unixsunset).strftime('%H:%M:%S')
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)

        return data_temp, data_cloud, normal_sunrise, normal_sunset, current_time
    else:
        print('error: got response code %d' % response.status_code)
        print(response.text)
        return 0.0, 0.0

def weather_init(user_zip):
    zip_code = user_zip
    temp, cloud, sunrise, sunset,current = get_weather(zip_code)
    h1, m1, s1 = sunrise.split(':')
    sunrise_new = float(int(h1) * 3600 + int(m1) * 60 + int(s1))/3600
    h2, m2, s2 = sunset.split(':')
    sunset_new = float(int(h2) * 3600 + int(m2) * 60 + int(s2))/3600
    h3, m3, s3 = current.split(':')
    current_new = float(int(h3) * 3600 + int(m3) * 60 + int(s3))/3600
    # output_1 = '{:.1f}F, {:>.0f}% Cloudiness'.format(temp, cloud)
    # output_2 = '{} Sunrise, {} Sunset'.format(temp, cloud, sunrise, sunset)
    # print('weather for {}: {}'.format(zip_code, output))

    return sunrise_new, sunset_new, temp, cloud, current_new


WEATHER_APP = {
    'name': 'Weather',
    'init': weather_init
}


    