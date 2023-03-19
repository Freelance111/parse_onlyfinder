import pickle
import os
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GoogleSheet:
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    service = None

    def __init__(self, spreadsheet_id):
        creds = None
        if os.path.exists('creds/token.pickle'):
            with open('creds/token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                print('flow')
                flow = InstalledAppFlow.from_client_secrets_file(
                    'creds/credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open('creds/token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.SPREADSHEET_ID = spreadsheet_id
        self.service = build('sheets', 'v4', credentials=creds)

    def appendRangeValues(self, range, values):
        result = self.service.spreadsheets().values().append(
            spreadsheetId=self.SPREADSHEET_ID,
            range=range,
            valueInputOption='RAW',
            body={ 'values': values }).execute()
        print('{0} cells updated.'.format((result.get('updates'))["updatedRange"]))

    def batchUpdateRangeValues(self, data):
        body = {
            'valueInputOption': 'USER_ENTERED',
            'data': data
        }
        result = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=body).execute()
        print('{0} cells updated.'.format(result.get('totalUpdatedCells')))

    def getData(self, range):
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.SPREADSHEET_ID,
            range=range).execute()
        try:
            data = result['values']
            return data
        except KeyError:
            print("\tCheck the id of the table. The table is empty")
