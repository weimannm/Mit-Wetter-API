import pyowm
from datetime import datetime

API_KEY = '6d16db63c980c5a1628641c72b6d7a63'
COUNTRY = 'DE'

def getDateDelta():
    arrive = -1
    while arrive not in range(0, 6):
        #FIXME well anythin besides an int is gonna crash
        arrive = int(input("How many days are there (0 - 5) before you arrive? "))
    return arrive


def getLocation():
    owm = pyowm.OWM(API_KEY)
    valid_location = False
    while not valid_location:
        try:
            city_registry = owm.city_id_registry()
            # FIXME here i just take he first entry because its easier to handle
            cities = city_registry.locations_for(input("Which city or town are you visiting? "), COUNTRY)
            return cities[0]
        except:
            print('The entered location can not be found, make sure it is located in ' + COUNTRY)


def getWeather(location, dateDelta):
    owm = pyowm.OWM(API_KEY)
    mgr = owm.weather_manager()
    one_call = mgr.one_call(lat=location.lat, lon=location.lon, units='metric')
    weather_data = one_call.forecast_daily[dateDelta]
    return weather_data


def generateMessage(weather_data):
    print("The weather on %s will be %s, %s to be exact." % (
        datetime.utcfromtimestamp(weather_data.reference_time()).strftime('%d-%m-%Y'),
        weather_data.status, weather_data.detailed_status))
    print("The sun will rise at %s and set at %s." %
          (datetime.utcfromtimestamp(weather_data.sunrise_time()).strftime('%H:%M'),
           datetime.utcfromtimestamp(weather_data.sunset_time()).strftime('%H:%M')))
    temp_mean = (weather_data.temperature()['min'] + weather_data.temperature()['max']) / 2
    print("The temperature will be between %s and %s" % (weather_data.temperature()['min'],
                                                         weather_data.temperature()['max']))
    if temp_mean <= 5.0:
        print("You better wear a warm coat. It's gonna be bone-chilling cold.")
    elif 5.0 < temp_mean <= 10.0:
        print("Wear a jacket. It's cold outside.")
    elif 10.0 < temp_mean <= 20.0:
        print("Grab a jacket or warm sweater. Temperature seems to be alright")
    elif 20.0 < temp_mean <= 25.0:
        print("A sweatshirt will be fine. It's warm")
    elif temp_mean > 25.0:
        print("A shirt will be more than enough. It's hot outside.")
    else:
        print("Wear whatever you desire.... I don't know  what this weather is")

    if weather_data.clouds >= 33:
        print("The sky is gonna be almost clear")
    elif 33 < weather_data.clouds <= 66:
        print("You might spot some clouds")
    elif 66 < weather_data.clouds:
        print("It's gonna be cloudy.")
    else:
        print("I don't even know if these are couds anymore...")

    if weather_data.rain['all'] <= 0.25:
        print("No rain in sight.")
    elif 0.25 < weather_data.rain['all'] <= 0.5:
        print("You might consider a slicker.")
    elif 0.5 < weather_data['all'] <= 0.75:
        print("You might consider an umbrella.")
    elif 0.75 < weather_data['all']:
        print("You'll need an umbrella!")
    else:
        print("This might be worse than rain!")

    # idk what damn unit this is... i assume km/h
    print("The wind will be %s km/h" %(weather_data.wind()['speed']))
    if weather_data.wind()['speed']<= 20.0:
        print("You won't notice the wind.")
    elif weather_data.wind()['speed'] <= 60.0:
        print("You might feel a breeze.")
    elif weather_data.wind()['speed']:
        print("Yoo will probably fly!")
    else:
        print("RUN!!!!!!")


if __name__ == '__main__':
    generateMessage(getWeather(getLocation(), getDateDelta()))


# OpenWaetherMap API Data
# jeston.legacy@schabernack.ru
# jestonlegacy
# J3sT0N$1
# 6d16db63c980c5a1628641c72b6d7a63

# srcs
# https://pyowm.readthedocs.io/en/latest/v3/code-recipes.html?highlight=daily_forecast
# https://projects.raspberrypi.org/en/projects/dress-for-the-weather
# https://pyowm.readthedocs.io/en/latest/v3/code-recipes.html#identifying_places
# https://pyowm.readthedocs.io/en/latest/pyowm.weatherapi25.html

