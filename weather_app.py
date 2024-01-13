from tkinter import *
import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import ttkbootstrap
from geopy.geocoders import Nominatim

def get_weather_by_coords(latitude, longitude):
    API_key = "api_key" 
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={API_key}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror('Error', 'City not found')
        return None

    # Parse the response JSON to get weather information
    weather = res.json()
    return parse_weather_response(weather)

def get_weather_by_city(city):  
    API_key = "api_key"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror('Error', 'City not found')
        return None

    # Parse the response JSON to get weather information
    weather = res.json()
    return parse_weather_response(weather)

def parse_weather_response(weather):
    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp'] - 273.15
    description = weather['weather'][0]['description']
    city = weather['name']
    country = weather['sys']['country']
    min_temp = weather['main']['temp_min'] - 273.15
    max_temp = weather['main']['temp_max'] - 273.15
    humidity = weather['main']['humidity']
    wind_speed = weather['wind']['speed']
    snowfall = weather.get('snow', {}).get('1h', 0)
    visibility = weather['visibility']

    # Get the icon URL and return all the weather information
    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (icon_url, temperature, description, city, country, min_temp, max_temp, humidity, wind_speed, snowfall, visibility)


def get_coordinates_from_address(address):
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        messagebox.showerror('Error', 'Location not found')
        return None, None

def search():
    city = city_entry.get()
    result = get_weather_by_city(city)
    if result is None:
        return
    update_weather_display(result)

def use_gps():  # uses the geopy library to convert a location name (e.g., "New York City") to GPS coordinates
    address = "Lagos"  # Replace with the desired default location
    latitude, longitude = get_coordinates_from_address(address)
    if latitude is not None and longitude is not None:
        result = get_weather_by_coords(latitude, longitude)
        if result is not None:
            update_weather_display(result)

def update_weather_display(result):
    icon_url, temperature, description, city, country, min_temp, max_temp, humidity, wind_speed, snowfall, visibility = result
    location_label.configure(text=f"{city}, {country}")

    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon

    temperature_label.configure(text=f"Temperature: {temperature:.2f}°C (Min: {min_temp:.2f}°C, Max: {max_temp:.2f}°C)")
    description_label.configure(text=f"Description: {description}")

    humidity_label.configure(text=f"Humidity: {humidity}%")
    wind_speed_label.configure(text=f"Wind Speed: {wind_speed} m/s")
    snowfall_label.configure(text=f"Snowfall (last 1h): {snowfall} mm")
    visibility_label.configure(text=f"Visibility: {visibility} meters")

root = ttkbootstrap.Window(themename='morph')
root.title('Weather App')
root.geometry('400x500')

# Entry widget to enter city name manually
city_entry = ttkbootstrap.Entry(root, font='Helvetica, 18')
city_entry.pack(pady=10)

# Button widget to search by city name
search_button = ttkbootstrap.Button(root, text='Search', command=search, bootstyle='warning')
search_button.pack(pady=10)

# Button widget to use GPS for automatic detection
gps_button = ttkbootstrap.Button(root, text='Use GPS', command=use_gps, bootstyle='success')
gps_button.pack(pady=10)


# Label widget to show the city/country name
location_label = tk.Label(root, font='Helvetica, 25')
location_label.pack(pady=20)

# To show the weather icon
icon_label = tk.Label(root)
icon_label.pack()

# Label widget to show the temperature
temperature_label = tk.Label(root, font='Helvetica, 20')
temperature_label.pack()

# To show the weather description
description_label = tk.Label(root, font='Helvetica, 20')
description_label.pack()

# Label widgets to show additional weather details
humidity_label = tk.Label(root, font='Helvetica, 15')
humidity_label.pack()

wind_speed_label = tk.Label(root, font='Helvetica, 15')
wind_speed_label.pack()

snowfall_label = tk.Label(root, font='Helvetica, 15')
snowfall_label.pack()

visibility_label = tk.Label(root, font='Helvetica, 15')
visibility_label.pack()

root.mainloop()
