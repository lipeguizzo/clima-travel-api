from django.http import JsonResponse
from django.views import View
import json
import pandas as pd
from core.settings import PATH_CSV
from enum import Enum

class EMonths(Enum):
    JANUARY = 'JANUARY',
    FEBRUARY = 'FEBRUARY',
    MARCH = 'MARCH',
    APRIL = 'APRIL',
    MAY = 'MAY',
    JUNE = 'JUNE',
    JULY = 'JULY',
    AUGUST = 'AUGUST',
    SEPTEMBER = 'SEPTEMBER',
    OCTOBER = 'OCTOBER',
    NOVEMBER = 'NOVEMBER',
    DECEMBER = 'DECEMBER',

    def enum_values():
        return [ value for value in EMonths ]

class EMonthsTranslate(Enum):
    JANUARY = 'JANEIRO'
    FEBRUARY = 'FEVEREIRO'
    MARCH = 'MARÇO'
    APRIL = 'ABRIL'
    MAY = 'MAIO'
    JUNE = 'JUNHO'
    JULY = 'JULHO'
    AUGUST = 'AGOSTO'
    SEPTEMBER = 'SETEMBRO'
    OCTOBER = 'OUTUBRO'
    NOVEMBER = 'NOVEMBRO'
    DECEMBER = 'DEZEMBRO'

    def enum_values():
        return [ value for value in EMonthsTranslate ]


class ClimateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            city = data.get('city')
            month = data.get('month')

            if( city == None or city == 'NONE' or month == None or month == 'NONE'):
                raise ValueError('Campo de cidade ou mês não preechidos!')
            elif( EMonths[month] not in EMonths.enum_values() ):
                raise ValueError('Mês inválido!')
            else:

                field_query = 'CODIGO'
                field_year = 'ANO'
                month_translate = EMonthsTranslate[month].value
                
                # Reading csv files
                df_precipitation = pd.read_csv(f'{PATH_CSV}/precipitation.csv', on_bad_lines='skip', sep=';')
                df_temperature_max = pd.read_csv(f'{PATH_CSV}/temperature-max.csv', on_bad_lines='skip', sep=';')
                df_temperature_min = pd.read_csv(f'{PATH_CSV}/temperature-min.csv', on_bad_lines='skip', sep=';')
                df_humidity= pd.read_csv(f'{PATH_CSV}/humidity.csv', on_bad_lines='skip', sep=';')
                df_wind = pd.read_csv(f'{PATH_CSV}/wind.csv', on_bad_lines='skip', sep=';')

                # Getting the precipitation
                df_precipitation_query = df_precipitation.query(f'{field_query} == {city}').index[0]
                precipitation = df_precipitation.at[df_precipitation_query, month_translate]
                precipitation_year = df_precipitation.at[df_precipitation_query, field_year]
                
                # Getting the temperature max
                df_temperature_max_query = df_temperature_max.query(f'{field_query} == {city}').index[0]
                temperature_max = df_temperature_max.at[df_temperature_max_query, month_translate]

                # Getting the temperature min
                df_temperature_min_query = df_temperature_min.query(f'{field_query} == {city}').index[0]
                temperature_min = df_temperature_min.at[df_temperature_min_query, month_translate]
                
                # Getting the humidity
                df_humidity_query = df_humidity.query(f'{field_query} == {city}').index[0]
                humidity = df_humidity.at[df_humidity_query, month_translate]
                humidity_year = df_humidity.at[df_humidity_query, field_year]

                # Getting the wind
                df_wind_query = df_humidity.query(f'{field_query} == {city}').index[0]
                wind = df_wind.at[df_wind_query, month_translate]
                wind_year = df_wind.at[df_wind_query, field_year]

                return JsonResponse({
                    'month': month,
                    'city': city,
                    'precipitation': precipitation,
                    'precipitationYear': precipitation_year,
                    'temperatureMax': temperature_max,
                    'temperatureMin': temperature_min,
                    'humidity': humidity,
                    'humidityYear': humidity_year,
                    'wind': wind,    
                    'windYear': wind_year    
                }, status=200)

        except IndexError as error:
            return JsonResponse({
                'message': 'Cidade inválida!'
            }, status=400)
        
        except Exception as error:  
            return JsonResponse({
                'message': str(error)
            }, status=400)
