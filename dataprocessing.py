from api import api
import pandas as pd

#Necessary Class to recieve dictionary of date(time), temp, and precip from JSON
class DailyWeather:
    def __init__(self, time, temperature_2m_mean, precipitation_sum):
        self.time = time
        self.temperature_2m_mean = temperature_2m_mean
        self.precipitation_sum = precipitation_sum

#Necessary Class to recieve dictionary of daily weather from JSON
class WeatherData:
    def __init__ (self, daily):
        self.daily = DailyWeather(**daily)
    
   
class jsonFileProcessing:
    def __init__ (self):
     '''Constructor function which assigns api html and creates instance of api class'''
     apiWebsite = "https://archive-api.open-meteo.com/v1/archive?latitude=43.81&longitude=-111.78&start_date=1940-01-01&end_date=2024-01-01&daily=temperature_2m_mean,precipitation_sum&temperature_unit=fahrenheit&precipitation_unit=inch&timezone=America%2FDenver"
     self.apiInstance = api(apiWebsite)
     self.jsonWeatherData = self.apiInstance.fetchApiData()
    
    def jsonFileDeserializer(self):
        '''Processes JSON file extracting values using instance of api class along with WeatherData and DailyWeather'''
        times = self.jsonWeatherData['daily']['time']
        temperatures = self.jsonWeatherData['daily']['temperature_2m_mean']
        precipitation = self.jsonWeatherData['daily']['precipitation_sum']
        
        #custom data structure using pandas to fomrat values
        dataframe = pd.DataFrame({
            'date' : times,
            'temperature' : temperatures,
            'precipitation' : precipitation
        })

        dataframe['date'] = pd.to_datetime(dataframe['date'])
        dataframe['year'] = dataframe['date'].dt.year
        average_temperatures_and_precipitation = dataframe.groupby('year').agg({
            'temperature' : 'mean',
            'precipitation' : 'sum'
        }).reset_index()
        
        

        return average_temperatures_and_precipitation
        

        




    


        

        

