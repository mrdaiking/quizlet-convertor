from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import csv
import pandas as pd

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
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
                'credentials2.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


def readFile():
    file = open('doushi1.csv')
    csvreader = csv.reader(file)
    header = next(csvreader)
    print(header)
    rows = []
    for row in csvreader:
        print(row.index(1))
        rows.append(row)
    # print(rows)
    file.close()


def readNewWords():
    # Creating the dataframe
    df = pd.read_csv("doushi1.csv")

    # column index value of "Name" column is 0
    # We have set takeable = True
    # to interpret the index / col as indexer
    # value = df._get_value(4, 1, takeable=True)
    # print((df['読み方']).to_string(index=False))
    # print(value)
    df = df[['言葉', '読み方', '意味', '例文']]
    df['Value'] = ";"+df['読み方'].astype(str) + "-" + df['意味'].astype(str) + "-" + df['例文'].astype(str)
    df = df[['言葉', 'Value']]
    print(df.to_string(index=False))

def readKanji():
    # Creating the dataframe
    df = pd.read_csv("kanji.csv")

    # column index value of "Name" column is 0
    # We have set takeable = True
    # to interpret the index / col as indexer
    # value = df._get_value(4, 1, takeable=True)
    # print((df['読み方']).to_string(index=False))
    # print(value)
    df = df[[ 'Kanji','Han', 'Kun', 'On', 'Collocation', 'Oboekata']]
    df['Value'] = ";" + df['Han'].astype(str) + "-" + df['Kun'].astype(str) +  df['On'].astype(str) + "-" + df['Collocation'].astype(str) + "-" + df['Oboekata'].astype(str)
    df = df[['Kanji', 'Value']]
    print(df.to_string(index=False))

if __name__ == '__main__':
    # readFile()
    # readNewWords()
    readKanji()
    # main()
