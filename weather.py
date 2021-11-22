import requests
import os
import discord
import datetime

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
    print("Logged in: {}\n".format(client.user.name))

@client.command()
async def current(ctx, city):

    await ctx.send("Would you like Fahrenheit or Celsius?")

    def check(m):
        return m.content in ['Fahrenheit', 'fahrenheit', 'f', 'F', 'Celsius', 'celsius', 'c', 'C'] and m.channel == ctx.channel

    msg = await client.wait_for("message", check=check)

    api_key = os.getenv('API_KEY')

    # Calling API url for Current Weather
    api_url = "https://api.openweathermap.org/data/2.5/weather?"

    # Adding user input of city and bot API key to api_url
    full_url = api_url + "q=" + city + "&appid=" + api_key

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

        # Calling wind speed and direction
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

        # Calling sunrise and sunset times
        sys_data = weather_data['sys']
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
                title="The current weather for {}".format(city.title()),
                url=f"https://openweathermap.org/city/{api_id}",
                description="Cloud Cover: {}".format(weather_description),
                color=discord.Color.blue()
            )

            embed.set_footer(text='Weather Bot')
            #embed.set_image(url='https://upload.wikimedia.org/wikipedia/commons/f/f6/OpenWeather-Logo.jpg')
            embed.set_thumbnail(url=f'http://openweathermap.org/img/wn/{api_image}@2x.png')
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
            #embed.add_field(name='Wind Direction', value=direction, inline=True)
            embed.add_field(name='Sunrise', value=timestampsunrise.strftime('%I:%M %p'), inline=True)
            embed.add_field(name='Sunset', value=timestampsunset.strftime('%I:%M %p'), inline=True)
            embed.add_field(name='\u200B', value='\u200B', inline=True)

            await ctx.send(embed=embed)

        elif msg.content == 'Celsius' or msg.content == 'celsius' or msg.content == 'c' or msg.content == 'C':
            embed = discord.Embed(
                title="The current weather for {}".format(city.title()),
                url=f"https://openweathermap.org/city/{api_id}",
                description="Cloud Cover: {}".format(weather_description),
                color=discord.Color.blue()
            )

            embed.set_footer(text='Weather Bot')
            #embed.set_image(url='https://upload.wikimedia.org/wikipedia/commons/f/f6/OpenWeather-Logo.jpg')
            embed.set_thumbnail(url=f'http://openweathermap.org/img/wn/{api_image}@2x.png')
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
            #embed.add_field(name='Wind Direction', value=direction, inline=True)
            embed.add_field(name='Sunrise', value=timestampsunrise.strftime('%I:%M %p'), inline=True)
            embed.add_field(name='Sunset', value=timestampsunset.strftime('%I:%M %p'), inline=True)
            embed.add_field(name='\u200B', value='\u200B', inline=True)

            await ctx.send(embed=embed)

        else:
            await ctx.send("You did not choose Fahrenheit or Celsius. Please try the command again with the correct input.")

    else:
        await ctx.send("City not found. Please retry the command using !current [city]")

@client.command()
async def afd(ctx, nwscode):

    forecast_url = "https://forecast.weather.gov/product.php?site="

    # The full URL to pull up a NWS Area Forecast Discussion
    full_forecast_url = forecast_url + nwscode.upper() + "&issuedby=" + nwscode.upper() + "&product=AFD&format=txt&version=1&glossary=1"
    non_text_only_url = forecast_url + nwscode.upper() + "&issuedby=" + nwscode.upper() + "&product=AFD&format=CI&version=1&glossary=1"

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
async def guide(ctx):

    embed = discord.Embed(
        title="Weather Bot Guide",
        description="To use the commands from this weather bot, please use the **!** prefix. Listed below are the current commands that the bot offers.",
        color=discord.Color.blue()
        )

    embed.set_footer(text='Weather Bot')
    embed.set_author(name='Weather Bot')
    embed.add_field(name='Current Weather: ', value='!current **city**  # For exaxmple, **!current Chicago** displays the current weather for Chicago after your input of Fahrenheit or Celsius', inline=False)
    embed.add_field(name='NWS Area Forecast Discussion: ', value='!afd **three letter code**  # For example, **!afd TLH** displays the Tallahassee discussion.', inline=False)

    await ctx.send(embed=embed)


client.run(TOKEN)