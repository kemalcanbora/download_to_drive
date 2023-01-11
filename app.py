from tqdm import tqdm
from config import read_config
from google.oauth2 import service_account
from apiclient import discovery
from googleapiclient.http import MediaFileUpload
import requests
import certifi
import os


class DownloadToDrive:
    def __init__(self):
        self.scopes_list = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file']
        self.credentials_json = "credentials.json"
        self.data_sets = read_config()["dataset"]
        self.service = self.google_auth()
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

    def google_auth(self):
        credentials = service_account.Credentials.from_service_account_file(self.credentials_json, scopes=self.scopes_list)
        service = discovery.build('drive', 'v3', credentials=credentials, cache_discovery=False)

        return service

    def download(self, progress_decorator=tqdm):

        for item in self.data_sets:
            url = item["url"]
            print(f"Downloading {url}")
            body = {
                'name': item["name"],
                'title': item["name"],
                'description': item["name"],
                'mimeType': item["mimeType"],
                'parents': item["drive_path_id"]
            }

            response = requests.get(url,
                                    cert=certifi.where(),
                                    verify=False,
                                    stream=True,
                                    headers=self.header)
            total_size_in_bytes = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 Kibibyte
            progress_bar = progress_decorator(total=total_size_in_bytes, unit='iB', unit_scale=True)
            with open(item["name"], 'wb') as file:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)
            progress_bar.close()

            file = self.service.files().create(
                    supportsAllDrives=True,
                    body=body,
                    media_body=MediaFileUpload(filename=item["name"],
                                               mimetype=item["mimeType"])).execute()
            print("Uploaded file with ID {}".format(file.get('id')))
            os.remove(item["name"])

if __name__ == '__main__':
    DownloadToDrive().download()
