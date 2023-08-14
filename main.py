from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from functions import read_sheet, add_row, speed_test
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Execution timed out")

SAMPLE_SPREADSHEET_ID = os.getenv("SAMPLE_SPREADSHEET_ID")
SAMPLE_RANGE_NAME = os.getenv("SAMPLE_RANGE_NAME")

# Set the signal handler
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(45)

try:
    formatted_date, formatted_time, download_speed, upload_speed = speed_test()
    test_data = [[formatted_date, formatted_time, download_speed, upload_speed]]
    add_row(sheet_id=SAMPLE_SPREADSHEET_ID, 
            data_range=SAMPLE_RANGE_NAME, 
            data_list=test_data)
except TimeoutError:
    print("Execution timed out")
except Exception as e:
    print("An error occurred:", e)
finally:
    signal.alarm(0)  # Reset the alarm