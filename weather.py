import json
import urllib
import string
import re
from datetime import datetime
import time
import sys

hello = 1

hell = 2

#GPS = sys.argv[1]
GPS = "42.318156,-83.515020"

key = "9e2e91b105dc8b62348a42e247c51430"

data = urllib.urlopen("https://api.forecast.io/forecast/"+key+"/"+GPS).read()
data = json.loads(data)

currentSummary = data["currently"]["summary"]
currentTemp = data["currently"]["temperature"]
currentAppTemp = data["currently"]["apparentTemperature"]
currentIconRaw = data["currently"]["icon"]
currentIconURL = "http://www.kaiserfamilyband.com/BCPC/WeatherIcons/"+currentIconRaw+".png"
if currentIconRaw == "clear-day" or currentIconRaw == "clear-night":
    currentIcon = "ic_action_sun"
elif currentIconRaw == "cloudy":
    currentIcon = "ic_action_cloud"
elif currentIconRaw == "fog":
    currentIcon = "ic_action_mist"
elif currentIconRaw == "hail" or currentIconRaw == "rain" or currentIconRaw == "sleet":
    currentIcon = "ic_action_rain"
elif currentIconRaw == "partly-cloudy-day" or currentIconRaw == "partly-cloudy-night":
    currentIcon = "ic_action_cloudy"
elif currentIconRaw == "snow":
    currentIcon = "device_access_brightness_low"
elif currentIconRaw == "thunderstorm":
    currentIcon = "ic_action_flash"
elif currentIconRaw == "tornado":
    currentIcon = "alerts_and_states_warning"
elif currentIconRaw == "wind":
    currentIcon = "ic_action_flag"
else:
    currentIcon = "ic_action_help"
currentWindSpeed = data["currently"]["windSpeed"]
currentWindBearing = data["currently"]["windBearing"]
if currentWindBearing < 11.25:
    currentWindBearing = "N"
elif currentWindBearing < 33.75:
    currentWindBearing = "NNE"
elif currentWindBearing < 56.25:
    currentWindBearing = "NE"
elif currentWindBearing < 78.75:
    currentWindBearing = "ENE"
elif currentWindBearing < 101.25:
    currentWindBearing = "E"
elif currentWindBearing < 123.75:
    currentWindBearing = "ESE"
elif currentWindBearing < 146.25:
    currentWindBearing = "SE"
elif currentWindBearing < 168.75:
    currentWindBearing = "SSE"
elif currentWindBearing < 191.25:
    currentWindBearing = "S"
elif currentWindBearing < 213.75:
    currentWindBearing = "SSW"
elif currentWindBearing < 236.25:
    currentWindBearing = "SW"
elif currentWindBearing < 258.75:
    currentWindBearing = "WSW"
elif currentWindBearing < 281.25:
    currentWindBearing = "W"
elif currentWindBearing < 303.75:
    currentWindBearing = "WNW"
elif currentWindBearing < 326.75:
    currentWindBearing = "NW"
elif currentWindBearing < 348.75:
    currentWindBearing = "NNW"
else:
    currentWindBearing = "N"
currentPrecipProb = data["currently"]["precipProbability"]
currentHumidity = data["currently"]["humidity"]
hourlySummary = data["minutely"]["summary"]
dailySummary = data["hourly"]["summary"]
dailySummary = re.sub('[^\s!-~]', '-', dailySummary)
dailyHigh = data["daily"]["data"][0]["temperatureMax"]
dailyLow = data["daily"]["data"][0]["temperatureMin"]
sunriseTime = data["daily"]["data"][0]["sunriseTime"]
sunsetTime = data["daily"]["data"][0]["sunsetTime"]
weeklySummary = data["daily"]["summary"]
weeklySummary = filter(lambda x: x in string.printable, weeklySummary)

if "alerts" in data:
    alertTitle = data["alerts"][0]["title"]
    alertDesc = data["alerts"][0]["description"]
    alertDesc = string.replace(alertDesc, '\n', ' ')
    alertDesc = string.replace(alertDesc, " *", "\n*")
    alertURL = data["alerts"][0]["uri"]
else:
    alertTitle = " "
    alertDesc = " "
    alertURL = "about:blank"

days = []

for day in data["daily"]["data"]:
    days.append({})
    days[len(days)-1]["day"] = day["time"]
    days[len(days)-1]["icon"] = day["icon"]
    days[len(days)-1]["icon"] = string.replace(days[len(days)-1]["icon"],"night","day")
    days[len(days)-1]["high"] = day["temperatureMax"]
    days[len(days)-1]["low"] = day["temperatureMin"]
    if "precipAccumulation" in day:
        days[len(days)-1]["precip"] = day["precipAccumulation"]
    else:
        days[len(days)-1]["precip"] = 0.0
    days[len(days)-1]["precipProb"] = day["precipProbability"]

sys.stdout.write("weather=::="+currentSummary+"=.=")
sys.stdout.write("{0:.0f}".format(currentTemp)+"=.=")
sys.stdout.write(currentIconRaw+"=.=")
sys.stdout.write(currentIcon+"=.=")
sys.stdout.write(currentIconURL+"=.=")
sys.stdout.write("{0:.0f}".format(currentWindSpeed)+"=.=")
sys.stdout.write(currentWindBearing+"=.=")
sys.stdout.write("{0:.00f}".format(currentPrecipProb*100)+"=.=")
sys.stdout.write("{0:.00f}".format(currentHumidity*100)+"=.=")
sys.stdout.write(hourlySummary+"=.=")
sys.stdout.write(dailySummary+"=.=")
sys.stdout.write("{0:.0f}".format(dailyHigh)+"=.=")
sys.stdout.write("{0:.0f}".format(dailyLow)+"=.=")
sys.stdout.write(datetime.fromtimestamp(sunriseTime).strftime('%I:%M')+"=.=")
sys.stdout.write(datetime.fromtimestamp(sunsetTime).strftime('%I:%M')+"=.=")
sys.stdout.write(weeklySummary+"=.=")
sys.stdout.write(alertTitle+"=.=")
sys.stdout.write(alertDesc+"=.=")
sys.stdout.write(alertURL+"=.=")

for k in range(1,len(days)):
    sys.stdout.write(datetime.fromtimestamp(days[k]["day"]).strftime('%A')+"=.=")
    sys.stdout.write(days[k]["icon"]+"=.=")
    sys.stdout.write("{0:.0f}".format(days[k]["high"])+"=.=")
    sys.stdout.write("{0:.0f}".format(days[k]["low"])+"=.=")
    sys.stdout.write("{0:.0f}".format(days[k]["precipProb"]*100)+"=.=")
    sys.stdout.write("{0:.1f}".format(days[k]["precip"])+"=.=")

sys.stdout.write("{0:.0f}".format(currentTemp)+"=.=")
