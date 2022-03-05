import requests, os, discord, datetime, time, asyncio

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = commands.Bot(command_prefix="!")

directionDegrees = [350,360,0,10,11,39,40,59,80,100,100,
                 129,130,149,150,169,170,190,219,220,
                 239,240,259,260,280,281,309,310,329]

directions = ['N','N','N','N','N/NE','N/NE','E/NE',
              'E/NE','E','E','E/SE','E/SE','SE','SE',
              'S/SE','S/SE','S','S','S/SW','S/SW','SW',
              'SW','W/SW','W/SW','W','W','W/NW','W/NW',
              "NW",'N/NW']

def c2F(inp):
    return round((inp - 273.15) * (9 / 5) + 32)

def f2C(inp):
    return round((inp-273.15))

def rounder(inp):
    for i in range(len(directions) -1):
        if inp == directionDegrees[i]:
            return directionDegrees[i]
        else:
            return min(directionDegrees, key=lambda x: abs(x - inp))

@client.event
async def on_ready():
    print(f"Logged in: {client.user.name}\n")

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
        temperature, feels_like = main_data['temp'], main_data['feels_like']
        minimum_temp, maximum_temp = main_data['temp_min'], main_data['temp_max']
        pressure, humidity = main_data['pressure'], main_data['humidity']
        longitude = weather_data['coord']['lon']

        # Why not group the variables by how it's called in the embed with commas?

        # Calling wind speed, gust and direction
        wind_data, wind_speed = weather_data['wind'], wind_data['speed']
        wind_direction = wind_data['deg']

        rounded = rounder(wind_direction) # reference
        directionDegrees.index(rounded)

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

        if msg.content.upper() == 'Fahrenheit' or msg.content == 'F':
            embed = discord.Embed(
            title=f"The current weather for {cityjoin.title()}, {country.upper()}")
            url=f"https://openweathermap.org/city/{api_id}",
            description=f"Cloud Cover: {weather_description}"
            color=discord.Color.blue()
            )

            embed.set_footer(text='Weather Bot')
            #embed.set_image(url='https://upload.wikimedia.org/wikipedia/commons/f/f6/OpenWeather-Logo.jpg')
            embed.set_thumbnail(url=f'http://openweathermap.org/img/wn/{api_image}@3x.png')
            embed.set_author(name='Weather Bot')
            embed.add_field(name='Temperature', value=f"{c2F(temperature)}°F", inline=True)
            embed.add_field(name='Feels Like', value=f"{c2F(feels_like)}°F", inline=True)
            embed.add_field(name='\u200B', value='\u200B', inline=True)
            embed.add_field(name='Maximum Temperature', value=f"{c2F(maximum_temp)}°F", inline=True)
            embed.add_field(name='Minimum Temperature', value=f"{c2F(minimum_temp)}°F", inline=True)
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

            if 'snow' in weather_data:
                snow_data = weather_data['snow']
                if '1h' in snow_data:
                    snow_hr = snow_data['1h']
                    embed.add_field(name='Snow over last hour', value=f"{round(snow_hr/25.4,4)} in", inline=True)
                if '3h' in snow_data:
                    snow_3hr = snow_data['3h']
                    embed.add_field(name='Snow over last three hours', value=f"{round(snow_3hr/25.4,4)} in", inline=True)

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

            await ctx.send(embed=embed)

        if msg.content.upper() == 'Celsius' or msg.content == 'C':
            embed = discord.Embed( # can you not capitalize the send?
            title=f"The current weather for {cityjoin.title()}, {country.upper()}", # f-string adjust
            url=f"https://openweathermap.org/city/{api_id}",
            description=f"Cloud Cover: {weather_description}"
            color=discord.Color.blue()

            embed.set_footer(text='Weather Bot')
            #embed.set_image(url='https://upload.wikimedia.org/wikipedia/commons/f/f6/OpenWeather-Logo.jpg')
            embed.set_thumbnail(url=f'http://openweathermap.org/img/wn/{api_image}@3x.png')
            embed.set_author(name='Weather Bot') # int(round((temperature-273.15)) we can write this as a function.
            embed.add_field(name='Temperature', value=f"{f2C(temperature)}°C", inline=True) # idk
            embed.add_field(name='Feels Like', value=f"{f2C(feels_like)}°C", inline=True)
            embed.add_field(name='\u200B', value='\u200B', inline=True)
            embed.add_field(name='Maximum Temperature', value=f"{f2C(maximum_temp)}°C", inline=True)
            embed.add_field(name='Minimum Temperature', value=f"{f2C(minimum_temp)}°C", inline=True)
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

            if 'snow' in weather_data:
                snow_data = weather_data['snow']
                if '1h' in snow_data:
                    snow_hr = snow_data['1h']
                    embed.add_field(name='Snow over last hour', value=f"{round(snow_hr,2)} mm", inline=True)
                if '3h' in snow_data: # elif
                    snow_3hr = snow_data['3h']
                    embed.add_field(name='Snow over last three hours', value=f"{round(snow_3hr,2)} mm", inline=True)

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
        title=f"The current Area Forecast Discussion for {nwscode.upper()}",
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