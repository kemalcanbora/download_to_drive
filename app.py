from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from tqdm import tqdm
from config import read_config
import os
import ssl
import urllib.request
import certifi


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

    def download(self, progress_decorator=tqdm):
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        for item in self.data_sets:
            url = item["url"]
            response = urllib.request.urlopen(url, context=ssl_context)
            file_size = int(response.info().get("Content-Length", -1))
            progress = progress_decorator(total=file_size, unit="iB", unit_scale=True)
            with open(item["name"], "wb") as f:
                while True:
                    data = response.read(1024)
                    if not data:
                        break
                    progress.update(len(data))
                    f.write(data)
            progress.close()
            if file_size != 0 and progress.n != file_size:
                print("ERROR, something went wrong")
            else:
                file = self.drive.CreateFile({'parents': [{'id': item["drive_path_id"]}],
                                              'title': item["name"]})
                file.SetContentFile(item["name"])
                file.Upload()
                print("Uploaded file with ID {}".format(file.get('id')))
                os.remove(item["name"])

if __name__ == '__main__':
    DownloadToDrive().download()
