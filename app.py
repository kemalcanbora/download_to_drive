from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import requests
from tqdm import tqdm
from config import read_config
import os


class DownloadToDrive:
    def __init__(self):
        self.credentials_path = os.getcwd()+"/credentials/saved_credentials.json"
        self.data_sets = read_config()["dataset"]
        self.drive = self.google_auth()
    def google_auth(self):
        g_auth = GoogleAuth()
        g_auth.LoadCredentialsFile(self.credentials_path)
        if g_auth.credentials is None:
            g_auth.LocalWebserverAuth()
        elif g_auth.access_token_expired:
            # Refresh them if expired
            g_auth.Refresh()
        else:
            # Initialize the saved creds
            g_auth.Authorize()
            # Save the current credentials to a file
        g_auth.SaveCredentialsFile(self.credentials_path)
        drive = GoogleDrive(g_auth)
        return drive

    def download(self, chuck_size=1024):
        for item in self.data_sets:
            url = item["url"]
            r = requests.get(url, stream=True)
            with open(item["name"], 'wb') as f:
                for chunk in tqdm(r.iter_content(chunk_size=chuck_size)):
                    if chunk:
                        f.write(chunk)
                        f.flush()

                file = self.drive.CreateFile({'parents': [{'id': item["drive_path_id"]}],
                                              'title': item["name"]})
                file.SetContentFile(item["name"])
                file.Upload()
                print("Uploaded file with ID {}".format(file.get('id')))
                os.remove(item["name"])

if __name__ == '__main__':
    DownloadToDrive().download()
