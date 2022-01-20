import requests
import os
import discord
import datetime
import time
import asyncio

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
    print("Logged in: {}\n".format(client.user.name))

@client.command()
async def current(ctx, *city):

    await ctx.send("Would you like Fahrenheit or Celsius?")

    def check(m):
        return m.content in ['Fahrenheit', 'fahrenheit', 'f', 'F', 'Celsius', 'celsius', 'c', 'C'] and m.channel == ctx.channel

    msg = await client.wait_for("message", check=check)

    api_key = os.getenv('API_KEY')

    cityjoin = " ".join(city)

    # Calling API url for Current Weather
    api_url = "https://api.openweathermap.org/data/2.5/weather?"

    # Adding user input of city and bot API key to api_url
    full_url = api_url + "q=" + cityjoin + "&appid=" + api_key

    # Using responses import to make a GET request to API
    response = requests.get(full_url)

    if response.status_code == 200:
        weather_data = response.json()

        # Calling main data
        main_data = weather_data['main']

        # Calling the temperature, feels like temperature, minimum temperature, maximum temperature, pressure and humidity
        temperature = main_data['temp']
        feels_like = main_data['feels_like']
        minimum_temp = main_data['temp_min']
        maximum_temp = main_data['temp_max']
        pressure = main_data['pressure']
        humidity = main_data['humidity']
        longitude = weather_data['coord']['lon']
        latitude = weather_data['coord']['lat']

        # Calling wind speed, gust and direction
        wind_data = weather_data['wind']
        wind_speed = wind_data['speed']
        wind_direction = wind_data['deg']


        if (wind_direction >= 350 and wind_direction <= 360) or (wind_direction >= 0 and wind_direction <= 10):
            direction = "N"
        elif wind_direction > 10 and wind_direction <= 39:
            direction = "N/NE"
        elif wind_direction >= 40 and wind_direction <= 59:
            direction = "NE"
        elif wind_direction >= 60 and wind_direction <= 79:
            direction = "E/NE"
        elif wind_direction >= 80 and wind_direction <= 100:
            direction = "E"
        elif wind_direction > 100 and wind_direction <= 129:
            direction = "E/SE"
        elif wind_direction >= 130 and wind_direction <= 149:
            direction = "SE"
        elif wind_direction >= 150 and wind_direction <= 169:
            direction = "S/SE"
        elif wind_direction >= 170 and wind_direction <= 190:
            direction = "S"
        elif wind_direction > 190 and wind_direction <= 219:
            direction = "S/SW"
        elif wind_direction >= 220 and wind_direction <= 239:
            direction = "SW"
        elif wind_direction >= 240 and wind_direction <= 259:
            direction = "W/SW"
        elif wind_direction >= 260 and wind_direction <= 280:
            direction = "W"
        elif wind_direction > 280 and wind_direction <= 309:
            direction = "W/NW"
        elif wind_direction >= 310 and wind_direction <= 329:
            direction = "NW"
        else:
            direction = "N/NW"


        # Calling sunrise and sunset times. Calling country of city.
        sys_data = weather_data['sys']
        country = sys_data['country']
        sunrise = sys_data['sunrise']
        sunset = sys_data['sunset']
        timezone = weather_data['timezone']

        timestampsunrise = datetime.datetime.utcfromtimestamp(sunrise + timezone)
        timestampsunset = datetime.datetime.utcfromtimestamp(sunset + timezone)

        # Calling weather information
        weather_info = weather_data['weather'][0]
        weather_description = weather_info['description'].title()
        api_image = weather_info['icon']

        # Calling city/state id code from API
        api_id = weather_data['id']

        if msg.content == 'Fahrenheit' or msg.content == 'fahrenheit' or msg.content == 'f' or msg.content == 'F':
            embed = discord.Embed(
                title="The current weather for {}, {}".format(cityjoin.title(), country.upper()),
                url=f"https://openweathermap.org/city/{api_id}",
                description="Cloud Cover: {}".format(weather_description),
                color=discord.Color.blue()
            )

            embed.set_footer(text='Weather Bot')
            #embed.set_image(url='https://upload.wikimedia.org/wikipedia/commons/f/f6/OpenWeather-Logo.jpg')
            embed.set_thumbnail(url=f'http://openweathermap.org/img/wn/{api_image}@3x.png')
            embed.set_author(name='Weather Bot')
            embed.add_field(name='Temperature', value=f"{int(round((temperature-273.15)*(9/5)+32))}°F", inline=True)
            embed.add_field(name='Feels Like', value=f"{int(round((feels_like-273.15)*(9/5)+32))}°F", inline=True)
            embed.add_field(name='\u200B', value='\u200B', inline=True)
            embed.add_field(name='Maximum Temperature', value=f"{int(round((maximum_temp-273.15)*(9/5)+32))}°F", inline=True)
            embed.add_field(name='Minimum Temperature', value=f"{int(round((minimum_temp-273.15)*(9/5)+32))}°F", inline=True)
            embed.add_field(name='\u200B', value='\u200B', inline=True)
            embed.add_field(name='Humidity', value=f"{humidity}%", inline=True)
            embed.add_field(name='Pressure', value=f"{pressure} mb", inline=True)
            embed.add_field(name='Wind', value=f"{direction} at {int(round(wind_speed*1.15))} mph", inline=True)
            embed.add_field(name='Sunrise', value=timestampsunrise.strftime('%I:%M %p'), inline=True)
            embed.add_field(name='Sunset', value=timestampsunset.strftime('%I:%M %p'), inline=True)
            embed.add_field(name='\u200B', value='\u200B', inline=True)

            if 'rain' in weather_data:
                rain_data = weather_data['rain']
                if '1h' in rain_data:
                    rain_hr = rain_data['1h']
                    embed.add_field(name='Rain over last hour', value=f"{round(rain_hr/25.4,4)} in", inline=True)
                if '3h' in rain_data:
                    rain_3hr = rain_data['3h']
                    embed.add_field(name='Rain over last three hours', value=f"{round(rain_3hr/25.4,4)} in", inline=True)
                else:
                    pass
            else:
                pass

            if 'snow' in weather_data:
                snow_data = weather_data['snow']
                if '1h' in snow_data:
                    snow_hr = snow_data['1h']
                    embed.add_field(name='Snow over last hour', value=f"{round(snow_hr/25.4,4)} in", inline=True)
                if '3h' in snow_data:
                    snow_3hr = snow_data['3h']
                    embed.add_field(name='Snow over last three hours', value=f"{round(snow_3hr/25.4,4)} in", inline=True)
                else:
                    pass
            else:
                pass

            alerts_api_url = "https://api.openweathermap.org/data/2.5/onecall?lat="
            alerts_full_url = alerts_api_url + f'{latitude}' + "&lon=" + f'{longitude}' + "&appid=" + api_key

            alerts_response = requests.get(alerts_full_url)

            alerts_data = alerts_response.json()

            if 'alerts' in alerts_data:
                alerts = alerts_data['alerts'][0]
                sender_name = alerts['sender_name']
                event = alerts['event']
                start_of_alert = alerts['start']
                end_of_alert = alerts['end']
                timestampstart = datetime.datetime.utcfromtimestamp(start_of_alert + timezone)
                timestampend = datetime.datetime.utcfromtimestamp(end_of_alert + timezone)
                description = alerts['description']

                embed.add_field(name='\u200B', value='\u200B', inline=False)
                embed.add_field(name='Alerts', value=f'{event}', inline=True)
                embed.add_field(name='Start Time', value=timestampstart.strftime('%I:%M %p'), inline=True)
                embed.add_field(name='End Time', value=timestampend.strftime('%I:%M %p'), inline=True)
                embed.add_field(name='Description', value=f'{description}', inline=False)
            else:
                pass

            await ctx.send(embed=embed)

        elif msg.content == 'Celsius' or msg.content == 'celsius' or msg.content == 'c' or msg.content == 'C':
            embed = discord.Embed(
                title="The current weather for {}, {}".format(cityjoin.title(), country.upper()),
                url=f"https://openweathermap.org/city/{api_id}",
                description="Cloud Cover: {}".format(weather_description),
                color=discord.Color.blue()
            )

            embed.set_footer(text='Weather Bot')
            #embed.set_image(url='https://upload.wikimedia.org/wikipedia/commons/f/f6/OpenWeather-Logo.jpg')
            embed.set_thumbnail(url=f'http://openweathermap.org/img/wn/{api_image}@3x.png')
            embed.set_author(name='Weather Bot')
            embed.add_field(name='Temperature', value=f"{int(round((temperature-273.15)))}°C", inline=True)
            embed.add_field(name='Feels Like', value=f"{int(round((feels_like-273.15)))}°C", inline=True)
            embed.add_field(name='\u200B', value='\u200B', inline=True)
            embed.add_field(name='Maximum Temperature', value=f"{int(round((maximum_temp-273.15)))}°C", inline=True)
            embed.add_field(name='Minimum Temperature', value=f"{int(round((minimum_temp-273.15)))}°C", inline=True)
            embed.add_field(name='\u200B', value='\u200B', inline=True)
            embed.add_field(name='Humidity', value=f"{humidity}%", inline=True)
            embed.add_field(name='Pressure', value=f"{pressure} mb", inline=True)
            embed.add_field(name='Wind', value=f"{direction} at {int(round(wind_speed*1.852))} km/h", inline=True)
            embed.add_field(name='Sunrise', value=timestampsunrise.strftime('%I:%M %p'), inline=True)
            embed.add_field(name='Sunset', value=timestampsunset.strftime('%I:%M %p'), inline=True)
            embed.add_field(name='\u200B', value='\u200B', inline=True)

            if 'rain' in weather_data:
                rain_data = weather_data['rain']
                if '1h' in rain_data:
                    rain_hr = rain_data['1h']
                    embed.add_field(name='Rain over last hour', value=f"{round(rain_hr,2)} mm", inline=True)
                if '3h' in rain_data:
                    rain_3hr = rain_data['3h']
                    embed.add_field(name='Rain over last three hours', value=f"{round(rain_3hr,2)} mm", inline=True)
                else:
                    pass
            else:
                pass

            if 'snow' in weather_data:
                snow_data = weather_data['snow']
                if '1h' in snow_data:
                    snow_hr = snow_data['1h']
                    embed.add_field(name='Snow over last hour', value=f"{round(snow_hr,2)} mm", inline=True)
                if '3h' in snow_data:
                    snow_3hr = snow_data['3h']
                    embed.add_field(name='Snow over last three hours', value=f"{round(snow_3hr,2)} mm", inline=True)
                else:
                    pass
            else:
                pass

            alerts_api_url = "https://api.openweathermap.org/data/2.5/onecall?lat="
            alerts_full_url = alerts_api_url + f'{latitude}' + "&lon=" + f'{longitude}' + "&appid=" + api_key

            alerts_response = requests.get(alerts_full_url)

            alerts_data = alerts_response.json()

            if 'alerts' in alerts_data:
                alerts = alerts_data['alerts'][0]
                sender_name = alerts['sender_name']
                event = alerts['event']
                start_of_alert = alerts['start']
                end_of_alert = alerts['end']
                timestampstart = datetime.datetime.utcfromtimestamp(start_of_alert + timezone)
                timestampend = datetime.datetime.utcfromtimestamp(end_of_alert + timezone)
                description = alerts['description']

                embed.add_field(name='\u200B', value='\u200B', inline=False)
                embed.add_field(name='Alerts', value=f'{event}', inline=True)
                embed.add_field(name='Start Time', value=timestampstart.strftime('%I:%M %p'), inline=True)
                embed.add_field(name='End Time', value=timestampend.strftime('%I:%M %p'), inline=True)
                embed.add_field(name='Description', value=f'{description}', inline=False)
            else:
                pass

            await ctx.send(embed=embed)

        else:
            await ctx.send("You did not choose Fahrenheit or Celsius. Please try the command again with the correct input.")

    else:
        await ctx.send("City not found. Please retry the command using !current **city**")


@client.command()
async def afd(ctx, nwscode):

    forecast_url = "https://forecast.weather.gov/product.php?site="

    # The full URL to pull up a NWS Area Forecast Discussion
    full_forecast_url = forecast_url + nwscode.upper() + "&issuedby=" + nwscode.upper() + "&product=AFD&format=txt&version=1&glossary=1"
    non_text_only_url = forecast_url + nwscode.upper() + "&issuedby=" + nwscode.upper() + "&product=AFD&format=CI&version=1&glossary=1"

    readinghtml = requests.get(non_text_only_url)
    readinghtml.text

    if readinghtml.text == '<h3>Incorrect Template Request!</h3>':
        await ctx.send('Invalid NWS office. Type **!list** to find a list of valid NWS offices.')
    else:
        embed = discord.Embed(
        title="The current Area Forecast Discussion for {}".format(nwscode.upper()),
        url=non_text_only_url,
        description="Issued by the National Weather Service",
        color=discord.Color.blue()
        )

        embed.set_footer(text='Weather Bot')
        embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/US-NationalWeatherService-Logo.svg/1200px-US-NationalWeatherService-Logo.svg.png')
        embed.set_author(name='Weather Bot')

        await ctx.send(embed=embed)

@client.command()
async def list(ctx):

    list_afd_url = "https://forecast.weather.gov/product_sites.php?site=TAE&product=AFD"

    embed = discord.Embed(
    title="NWS Area Forecast Discussion Areas",
    url=list_afd_url,
    description="A list of NWS offices with available Area Forecast Discussions.",
    color=discord.Color.blue()
    )

    embed.set_footer(text='Weather Bot')
    embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/US-NationalWeatherService-Logo.svg/1200px-US-NationalWeatherService-Logo.svg.png')
    embed.set_author(name='Weather Bot')

    await ctx.send(embed=embed)


@client.command()
async def guide(ctx):

    embed = discord.Embed(
        title="Weather Bot Guide",
        description="To use the commands from this weather bot, please use the **!** prefix. Listed below are the current commands that the bot offers.",
        color=discord.Color.blue()
        )

    embed.set_footer(text='Weather Bot')
    embed.set_author(name='Weather Bot')
    embed.add_field(name='Current Weather: ', value='!current **city**  # For example, **!current Chicago** displays the current weather for Chicago after your input of Fahrenheit or Celsius', inline=False)
    embed.add_field(name='NWS Area Forecast Discussion: ', value='!afd **three letter code**  # For example, **!afd TAE** displays the Tallahassee discussion. Type **!list** to display valid three-letter identifiers.', inline=False)

    await ctx.send(embed=embed)


client.run(TOKEN)