# IMPORTS AND INITIALIZING THE DRIVE API
from __future__ import print_function
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from json import load, dump
import pandas as pd
from tqdm import tqdm
import os
SCOPES = ['https://www.googleapis.com/auth/drive']
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
service = build('drive', 'v3', credentials=creds)




# GETTING SOME INFO INCLUDING THE FILE ID OF THE FOLDER
with open("local_settings.json") as f:
    local_settings = load(f)
    IP = local_settings["IP"]
    PORT = local_settings["PORT"]
    people = local_settings["people"]

data = pd.read_csv(people).to_dict(orient="records")
DOMAIN = f"http://{IP}:{PORT}"
FOLDER_ID = local_settings.get("folder_id")
if FOLDER_ID is None:  # create a folder in Drive and get its ID
    folder_metadata = {
        "name": "Saraswati_Puja",
        "mimeType": "application/vnd.google-apps.folder"
    }
    FOLDER_ID = service.files().create(body = folder_metadata).execute()["id"]
    local_settings["folder_id"] = FOLDER_ID
    with open("local_settings.json", "w") as f:
        dump(local_settings, f)

def upload_file(file_name, file_type="image/png", folder_id=FOLDER_ID):
    file_metadata = {
        "name": file_name,
        "parents": [folder_id]
    }
    media = MediaFileUpload(f"./QRs/{file_name}", mimetype=file_type)
    file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    # print(f"File ID: {file.get('id')}")
    return file.get("id")

def give_permissions(file_id, email, name, count, role="reader"):
    
    message = f"""Hello {name}!
    Here is your QR code for the Saraswati Puja bhog. Please show this to the person at the door to get your bhog.
    
    Note: This QR code can be scanned only {count} times and will expire after that.
    
    Thank You,
    Saraswati Puja Committee
    """
    
    permission = {
        "type": "user",
        "role": role,
        "emailAddress": email,
    }
    
    service.permissions().create(
        fileId=file_id,
        body=permission,
        sendNotificationEmail=True,
        emailMessage = message
    ).execute()


l = os.listdir("QRs")

if len(l) < len(data):
    raise Exception(f"Not enough QR codes generated for all the people. Number of QR Code = {len(l)} and number of people = {len(data)}. Please generate {len(data) - len(l)} more QR codes before trying again.")

l = l[:len(data)]

new_data = {}

for qr, person in tqdm(list(zip(l, data))):
    file_id = upload_file(qr)
    give_permissions(file_id, person["email"], person["name"], person["count"])
    
    new_data[qr[:-4]] = person
    
    with open("stats.json", "w") as f:
        dump(new_data, f)