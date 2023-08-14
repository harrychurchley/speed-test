from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import speedtest
import time


def read_sheet(sheet_id, data_range):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range=data_range).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[4]))


def add_row(sheet_id, data_range, data_list):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    resource = {
        "majorDimension": "ROWS",
        "values": data_list
    }

    sheet = service.spreadsheets()
    sheet.values().append(
        spreadsheetId=sheet_id,
        range=data_range,
        valueInputOption='USER_ENTERED',
        body=resource
    ).execute()

    print("Added a new row to your Google sheet")

def speed_test():
    timestamp = time.time()
    formatted_date = time.strftime("%Y-%m-%d", time.localtime(timestamp))
    formatted_time = time.strftime("%H:%M:%S", time.localtime(timestamp))
    print(f"Time: {formatted_time}")
    st = speedtest.Speedtest()
    print("Getting best server...")
    st.get_best_server()

    print("Testing download speed...")
    download_speed = st.download() / 1024 / 1024  # Convert to Mbps
    print(f"Download Speed: {download_speed:.2f} Mbps")

    print("Testing upload speed...")
    upload_speed = st.upload() / 1024 / 1024  # Convert to Mbps
    print(f"Upload Speed: {upload_speed:.2f} Mbps")
    return formatted_date, formatted_time, download_speed, upload_speed