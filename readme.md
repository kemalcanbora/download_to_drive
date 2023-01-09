## How to generate drive API
   1. Create a new project in Google Developer Console by clicking “CREATE PROJECT” as
follows.
   2. Enable APIs and Services by clicking the “ENABLE APIS AND SERVICES”
   3. Click the “Google Drive API” icon and it will bring you to the next step as follows.
   4. Click the “ENABLE” button to enable the API.
   5. Create credentials by clicking the “CREATE CREDENTIALS”
   6. Desktop app 
   7. OAuth client ID
   8. Download the client configuration file and save it as “client_secret.json” in the

<b>Referance:</b> https://d35mpxyw7m7k7g.cloudfront.net/bigdata_1/Get+Authentication+for+Google+Service+API+.pdf

## How to use it?
 - Of course we're starting with `pip install -r requirements.txt`
 - Be sure to have `client_secrets.json` in the same directory as `app.py`
   - You can download in Google API Console
 - Edit the file `config.json`
 - Run `python3 app.py`
 - When you run the first time, you will be asked to authenticate with your Google account don't worry, it's safe.


