from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import matplotlib.pyplot as plt
import numpy as np

shopids=[]
shopidordersums=[]
custids=[]
numberOfRecurs=[]
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1xIQEm_tTyFsYYojQuUmu7QrF6wErlsOuy5-7wV9lCow'
SAMPLE_RANGE_NAME = 'A2:G5001'

def plotgraph():
    global custids, numberOfRecurs
    #put x axis labels here
    x=custids
    y=numberOfRecurs
    
    index=np.arange(len(x))
    plt.bar(index, y)
    
    #title axes
    plt.xlabel('Shop ids',fontsize=18)
    plt.ylabel('total value of orders (x10^7)',fontsize=18)
    
    #attach names to the xaxis points and rotate them to give enough space
    plt.xticks(index,x,fontsize=10,rotation=90)
    #title graph
    plt.title('total value of orders for each shop',fontsize=20)
    
    plt.show()
    

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    #else:
    #   print('Name, Major:')
    #   for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            #print('%s, %s' % (row[1], row[6]))
    else:
        # list shops and users
        global shopids, custids
        for row in values:
            if row[1] not in shopids:
                shopids.append(row[1])
            if row[2] not in custids:
                custids.append(row[2])
        #print(custids)
        # list number of times customers have made orders
        global numberOfRecurs
        for customer in custids:
            numberOfOrders=0
            for row in values:
                if row[2]==customer:
                    numberOfOrders+=1
            numberOfRecurs.append(numberOfOrders)
        print(numberOfRecurs)
                    
        # list shopid sums
        global shopidordersums
        for shopid in shopids:
            sums=0
            for row in values:
                if row[1]==shopid:
                    sums+=int(row[3])
            shopidordersums.append(sums)
        #print(shopidordersums)
        #plotgraph()
        
if __name__ == '__main__':
    main()