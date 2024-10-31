import googlesheets
from dataprocessing import jsonFileProcessing


if __name__ == "__main__":
    weather_processor = jsonFileProcessing() 
    average_temperatures_and_precipitation = weather_processor.jsonFileDeserializer()  
    googlesheets.load_json()

    boolean = googlesheets.create_spreadsheet()
    if boolean:
        googlesheets.add_data_to_spreadsheet(average_temperatures_and_precipitation)
        print('Success')
    else:
        print('Google Sheet was not created')
    
