
import requests




class api: 
    def __init__ (self, apiWebsite):
        self.apiWebsite = apiWebsite
    def fetchApiData(self):
        try: 
            responses = requests.get(self.apiWebsite)
            if responses.status_code == 200:
                data = responses.json()
                return data
            else:
                print("Failed to return json file from API", responses.status_code)

        except:
            print("An error has occured")
    
    



    
    
        
    
    