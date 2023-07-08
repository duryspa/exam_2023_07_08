from __future__ import print_function

import os.path
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from core import CONFIG


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = CONFIG.get('SPREADSHEET_ID')
TIMEZONE = int(CONFIG.get('TIMEZONE'))


def get_credentials():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds


def get_datetime():
    utc_time = datetime.datetime.utcnow().timestamp()
    
    local_datetime = (
        datetime.datetime.fromtimestamp(utc_time) 
        + datetime.timedelta(hours=TIMEZONE)
    ).strftime('%d.%m.%Y %H:%M:%S')

    return local_datetime


def record_values(username, text):
    creds = get_credentials()

    local_datetime = get_datetime()

    service = build('sheets', 'v4', credentials=creds)

    body = {
        'values': [[username, text, local_datetime]]
    }

    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID, range="A1:C1",
        valueInputOption="USER_ENTERED", body=body
    ).execute()

    if "updates" in result:
        if result.get('updates').get('updatedCells') == 3:
            return True

    return False
