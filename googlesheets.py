from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2.service_account import Credentials
import gspread
import json
import webbrowser


scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    ]
client = ''
creds = ''
worksheet_key = ''
spreadsheet_name = '80 Year Temperature and Precipitation Analysis for Rexburg, Idaho'
email = ''

def load_json():
    global client
    global creds
    file_path = input("Please copy and paste the file path of the api key into the terminal")

    try:
        with open(file_path, 'r') as f:
            info = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {file_path} wasnt found.")
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} isnt JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    creds = Credentials.from_service_account_info(info, scopes=scope)

    client = gspread.authorize(creds)



def create_spreadsheet():
    '''Originates the spreadsheet through the google api'''
    global worksheet_key
    spreadsheets = client.openall()

    if len(spreadsheets) != 0:
        for spreadsheet in spreadsheets:
            if spreadsheet.title == spreadsheet_name:
                print(f'The spreadsheet {spreadsheet_name} exists. Deleting it...')
                client.del_spreadsheet(spreadsheet.id)
                


            try:
                spreadsheet = client.create(spreadsheet_name)
                print(f'Spreadsheet {spreadsheet_name} was created successfully')
                worksheet_key = spreadsheet.id
                drive_service = build("drive", "v3", credentials=creds)
                drive_service.permissions().create(
                    fileId=worksheet_key,
                    body={
                        "type": "user",
                        "role": "writer",
                        "emailAddress": input("What is your google email?")  
        }
    ).execute()
                return True
            
            except Exception as e:
                print(f'There was an error {e}')
    else:
        spreadsheet = client.create(spreadsheet_name)
        print(f'Spreadsheet {spreadsheet_name} was created successfully')
        worksheet_key = spreadsheet.id
        drive_service = build("drive", "v3", credentials=creds)
        drive_service.permissions().create(
            fileId=worksheet_key,
            body={
                "type": "user",
                "role": "writer",
                "emailAddress": input("What is your google email?")   
        }
    ).execute()
        return True
            


def add_data_to_spreadsheet(data):
    '''Adds the deserialized data to the spreadsheet'''

    spreadsheet = client.open_by_key(worksheet_key)
    worksheet = spreadsheet.get_worksheet(0)

    worksheet.clear()
    data_to_insert = [data.columns.tolist()] + data.values.tolist()
    worksheet.insert_rows(data_to_insert, 1)

    
    #Line Graph in sheets on new sheet
    chart_request = {
        "addChart": {
            "chart": {
                "spec": {
                    "title": "83 Year Temperature and Precipitation Analysis for Rexburg, Idaho",
                    "basicChart": {
                        "chartType": "LINE",
                         "legendPosition": "TOP_LEGEND",
                        "axis": [
                            {
                                "position": "BOTTOM_AXIS",
                                "title": "Year",
                                "viewWindowOptions": {
                                    "viewWindowMin": 1940,
                                    "viewWindowMax": 2023
                                } 
                            },
                            {
                                "position": "LEFT_AXIS",
                                "title": "Temperature (°F)",
                                "viewWindowOptions": {
                                    "viewWindowMode": "PRETTY" 
                                } 
                            },
                            {
                                "position": "RIGHT_AXIS",
                                "title": "Precipitation (in)",
                                "viewWindowOptions": {
                                    "viewWindowMode": "PRETTY" 
                                } 
                            }
                        ],
                        "domains": [
                        {
                            "domain": {
                                "sourceRange": {
                                    "sources": [
                                        {
                                            "sheetId": worksheet.id,
                                            "startRowIndex": 1,  # Start after the header
                                            "endRowIndex": len(data_to_insert) - 1,  # Exclude the last year if needed
                                            "startColumnIndex": 0,
                                            "endColumnIndex": 1
                                        }
                                    ]
                                }
                            }
                        }
                    ],
                        "series": [
                            {
                                "series": {
                                    "sourceRange": {
                                        "sources": [
                                            {
                                                "sheetId": worksheet.id,
                                                "startRowIndex": 1,  # Start after the header
                                                "endRowIndex": len(data_to_insert) - 1,  # +1 for header
                                                "startColumnIndex": 1,
                                                "endColumnIndex": 2
                                            }
                                        ]
                                    }
                                }
                            },
                            {
                                "series": {
                                    "sourceRange": {
                                        "sources": [
                                            {
                                                "sheetId": worksheet.id,
                                                "startRowIndex": 1,
                                                "endRowIndex": len(data_to_insert) - 1,
                                                "startColumnIndex": 2,
                                                "endColumnIndex": 3
                                            }
                                        ]
                                    }
                                },
                                "targetAxis": "RIGHT_AXIS"
                            }
                        ]
                    }
                },
                "position": {
                    "newSheet": True  # Create the chart on a new sheet
                }
            }
        }
    }


    try:
       service = build("sheets", "v4", credentials=creds)
       service.spreadsheets().batchUpdate(
           spreadsheetId=worksheet_key,
           body={"requests": [chart_request]}
       ).execute()
       print(f"Created chart successfully")
    except Exception as e:
        print(f"Error in creating chart: {e}")


    url = worksheet.url
    webbrowser.open(url)

