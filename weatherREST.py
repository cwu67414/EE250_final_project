import requests
import datetime

# OpenWeatherMap API: https://openweathermap.org/current

# TODO: Sign up for an API key
OWM_API_KEY = 'a6868ed07eeb6ee1046d83ef083635f0'  # OpenWeatherMap API Key

class OnlineWeather(object):

    def get_weather(zip_code):
        params = {
            'appid': OWM_API_KEY,
            # TODO: referencing the API documentation, add the missing parameters for zip code and units (Fahrenheit)
            'zip': zip_code,
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

            return data_temp, data_cloud, normal_sunrise, normal_sunset
        else:
            print('error: got response code %d' % response.status_code)
            print(response.text)
            return 0.0, 0.0

    def weather_init(self):
        try:
            self.zip_code = int(input('ZIP:'))
        except ValueError:
            print("Not a number")

    def weather_results(self, data_temp, data_cloud, normal_sunrise, normal_sunset):

        temp = data_temp
        cloud = data_cloud
        sunrise = normal_sunrise
        sunset = normal_sunset
    
        output = '{:.1f}F, {:>.0f}% Cloudness, {} Sunrise, {} Sunset'.format(temp, cloud, sunrise, sunset)
        print('weather for {}: {}'.format(self.zip_code, output))

        return output

    WEATHER_APP = {
        'name': 'Weather',
        'init': weather_init
    }