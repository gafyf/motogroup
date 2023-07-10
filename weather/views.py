import requests, geocoder
from django.conf import settings
from django.shortcuts import render


def weather(request):
    api_key = settings.WEATHER_API_KEY
    if request.method == 'POST':
        location = request.POST.get('location', '')
        if location:
            current_url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}'
            forecast_url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=3&hour=24'
        else:
            return render(request, 'weather/weather.html', {'error': 'Please provide a location.'})
    else:
        api_key = settings.WEATHER_API_KEY
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        print('test ip nou: ', x_forwarded_for)
        if x_forwarded_for:
            user_ip = x_forwarded_for.split(',')[0]
        else:
            user_ip = request.META.get('REMOTE_ADDR')
        g = geocoder.ip(user_ip)
        latitude = g.lat
        longitude = g.lng
        approx_location = f"{latitude},{longitude}"        
        if approx_location:
            current_url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={approx_location}'
            forecast_url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={approx_location}&days=3&hour=24'
        else:
            return render(request, 'weather/weather.html', {'error': 'Latitude and longitude not finded.'})

    current_response = requests.get(current_url)
    current_data = current_response.json()
    forecast_response = requests.get(forecast_url)
    forecast_data = forecast_response.json()

    weather_data = {
        'location': {
            'name': current_data['location']['name'] if current_data['location']['name'] != 'None' else '',
            'region': current_data['location']['region'],
            'country': current_data['location']['country'],
            'localtime': current_data['location']['localtime'],
        },
        'current': {
            'temperature': current_data['current']['temp_c'],
            'condition': {
                'text': current_data['current']['condition']['text'],
                'icon': current_data['current']['condition']['icon'],
            },
            'wind_kph': current_data['current']['wind_kph'],
            'wind_degree': current_data['current']['wind_degree'],
            'wind_dir': current_data['current']['wind_dir'],
            'pressure_mb': current_data['current']['pressure_mb'],
            'precip_mm': current_data['current']['precip_mm'],
            'humidity': current_data['current']['humidity'],
            'cloud': current_data['current']['cloud'],
            'feelslike_c': current_data['current']['feelslike_c'],
        },
        'forecast': []
    }

    forecast_days = forecast_data['forecast']['forecastday']
    for forecast_day in forecast_days:
        forecast_day_date = forecast_day['date']
        forecast_day_mintemp = forecast_day['day']['mintemp_c']
        forecast_day_maxtemp = forecast_day['day']['maxtemp_c']
        forecast_day_maxwind = forecast_day['day']['maxwind_kph']
        forecast_day_totalprecip_mm = forecast_day['day']['totalprecip_mm']
        forecast_day_totalsnow_cm = forecast_day['day']['totalsnow_cm']
        forecast_day_avghumidity = forecast_day['day']['avghumidity']
        forecast_day_daily_will_it_rain = forecast_day['day']['daily_will_it_rain']
        forecast_day_daily_chance_of_rain = forecast_day['day']['daily_chance_of_rain']
        forecast_day_daily_will_it_snow = forecast_day['day']['daily_will_it_snow']
        forecast_day_daily_chance_of_snow = forecast_day['day']['daily_chance_of_snow']
        forecast_day_condition_text = forecast_day['day']['condition']['text']
        forecast_day_condition_icon = forecast_day['day']['condition']['icon']
        forecast_astro_sunrise = forecast_day['astro']['sunrise']
        forecast_astro_sunset = forecast_day['astro']['sunset']
        forecast_astro_is_moon_up = forecast_day['astro']['moonrise']
        forecast_astro_is_sun_up = forecast_day['astro']['moonset']

        weather_data['forecast'].append({
            'date': forecast_day_date,
            'mintemp': forecast_day_mintemp,
            'maxtemp': forecast_day_maxtemp,
            'maxwind': forecast_day_maxwind,
            'totalprecip_mm': forecast_day_totalprecip_mm,
            'totalsnow_cm': forecast_day_totalsnow_cm,
            'avghumidity': forecast_day_avghumidity,
            'daily_will_it_rain': forecast_day_daily_will_it_rain,
            'daily_chance_of_rain': forecast_day_daily_chance_of_rain,
            'daily_will_it_snow': forecast_day_daily_will_it_snow,
            'daily_chance_of_snow': forecast_day_daily_chance_of_snow,
            'condition_text': forecast_day_condition_text,
            'condition_icon': forecast_day_condition_icon,
            'sunrise': forecast_astro_sunrise,
            'sunset': forecast_astro_sunset,
            'is_moon_up': forecast_astro_is_moon_up,
            'is_sun_up': forecast_astro_is_sun_up,
        })

    return render(request, 'weather/weather.html', {'weather_data': weather_data})
  