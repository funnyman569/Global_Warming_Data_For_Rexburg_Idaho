# Global_Warming_Data_For_Rexburg_Idaho
 In this Python script, I deserialize a web-based JSON file that contains historic daily weather data and precipitation for Rexburg, Idaho summarized into annual median temperature and annual total precipitation. I then go on to write and graph this into Google Sheets.

# Development Environment
## Installation
No package installation required as i used a virutal enviroment which contains all the packages needed

## How to get API for Google. - necessary to be able to write to google sheets
• Go to https://console.cloud.google.com/   
• Sign into your google account   
• Inside google cloud create a new project (may have autointiazlied as "my first project"   
• Search "Google Sheets" in search bar at the top, click the first link, "Google Sheets API"   
• Click "Enable"   
• Repeat the previous two steps but this time searching "Google Drive API"   
• Search "Credentials" and click on the first link   
• On this page, at the top there will be a button that says "+ Create Credentials"   
• Click "Service Account"   
• Give your service account a name and description, role = basic, no users needed to grant permissions   
• Once you finish creating account, go back to the credentials page and click on your new service account link   
• Near the top, navigate to "Keys".   
• Click "Add Key", then select "Create new Key", then select JSON   
• This will automatically download a json file containing your google API key. Keep this SECURE   
• Pull down my code from github, drag and drop your api json file into your local repo   
• right click on the file containing your api and select "Copy Path"   

# Youtube Video Link
https://www.youtube.com/watch?v=nPytaM4uB7E

# Data Analysis Results
I wanted to determine by how many, if any, ºF had my hometown of Rexburg Idaho warmed up in the past 80 years. 
The data analysis shows that the average mean annual temperature has raised approx 3 ºF. I also showed total annual precipitation had decreased by about approx 3" as well

# Useful Websites
https://developers.google.com/sheets/api/samples/charts

