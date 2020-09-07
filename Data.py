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
# measure customer retention
retentionMetricForShops=[]
# Purchases Per Hour
purchasesPerHour=[]
Days=['M','Tu','W','Th','F','Sa','Su']
hours=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
purchasesPerDay=[]
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1xIQEm_tTyFsYYojQuUmu7QrF6wErlsOuy5-7wV9lCow'
SAMPLE_RANGE_NAME = 'A2:G5001'


def plotgraph():
    global Days, purchasesPerDay
    #put x axis labels here
    x=Days
    y=purchasesPerDay
    
    index=np.arange(len(x))
    plt.bar(index, y)
    
    #title axes
    plt.xlabel('Day of Sale',fontsize=18)
    plt.ylabel('Average Number of Sales',fontsize=18)
    
    #attach names to the xaxis points and rotate them to give enough space
    plt.xticks(index,x,fontsize=10,rotation=0)
    #title graph
    plt.title('Average Sales by Day of Week',fontsize=20)
    
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
    else:
        global purchasesPerHour
        # Time for sales
        for hour in range(24):
            buy=0
            for row in values:
                time=row[6][11:]
                if hour<10 and hour==int(time[0]) and time[1]==':':
                    buy+=1
                if hour>9 and len(time)==8:
                    if hour==int(time[0:2]):
                        buy+=1
            purchasesPerHour.append(buy)
        global purchasesPerDay
        W=[1,8,15,22,29]
        Th=[2,9,16,23,30]
        F=[3,10,17,24]
        Sa=[4,11,18,25]
        Su=[5,12,19,26]
        M=[6,13,20,27]
        Tu=[7,14,21,28]
        mon=0
        tue=0
        wed=0
        thu=0
        fri=0
        sat=0
        sun=0
        for row in values:
            date=row[6][8:10]
            if int(date) in W:
                wed+=1
            if int(date) in Th:
                thu+=1
            if int(date) in F:
                fri+=1
            if int(date) in Sa:
                sat+=1
            if int(date) in Su:
                sun+=1
            if int(date) in M:
                mon+=1
            if int(date) in Tu:
                tue+=1
        purchasesPerDay.append(mon/4)
        purchasesPerDay.append(tue/4)
        purchasesPerDay.append(wed/5)
        purchasesPerDay.append(thu/5)
        purchasesPerDay.append(fri/4)
        purchasesPerDay.append(sat/4)
        purchasesPerDay.append(sun/4)
        print(purchasesPerDay)
        
        # list shops and users
        global shopids, custids, retentionMetricForShops
        for row in values:
            if row[1] not in shopids:
                shopids.append(row[1])
            if row[2] not in custids:
                custids.append(row[2])
        # list number of times customers have made orders
        global numberOfRecurs
        for customer in custids:
            numberOfOrders=0
            for row in values:
                if row[2]==customer:
                    numberOfOrders+=1
            numberOfRecurs.append(numberOfOrders)         
        # list shopid sums
        global shopidordersums
        for shopid in shopids:
            sums=0
            for row in values:
                if row[1]==shopid:
                    sums+=int(row[3])
            shopidordersums.append(sums)
            

        #go to each shop
        for shop in shopids:
            userid=[]
            numberOfPurchasesByEachUser=[]
            #check each row
            for row in values:
                #if the current shop is seen and if the user associated with the order isn't already in the customer list, add them
                if (row[1]==shop) and (row[2] not in userid):
                    userid.append(row[2])
            #At this point we have a list of all customer who have made a purchase at the shop called userid
            #Now make a list of the number of times each of these users made a purchase specifically at this shop
            #Go to each user
            for user in userid:
                purchases=0
                #go through each row
                for row in values:
                    #if the current shop is found and the current user is matched with it, increase the number of purchases by 1
                    if (row[1]==shop) and (row[2]==user):
                        purchases+=1
                numberOfPurchasesByEachUser.append(purchases)
            #Now we have the number of purchases by all users who made a purchase at this particular shop and also the number of users who made a purchase
            averageRetention=sum(numberOfPurchasesByEachUser)/len(userid)
            retentionMetricForShops.append(averageRetention)

        # retention metric test
        # the retention metric for shop 46 came out to be 1, it seems as if all the users who made a purchase were unique so the following code was written to test the hypothesis (which turned out to be correct)
        lst=[]
        for row in values:
            if row[1]=='31':
              lst.append(row[2])
        if len(lst) > len(set(lst)):
            print('oh no!')
        elif len(lst)==len(set(lst)):
            print('Yes! Code is correct!')
        #plot a graph
        plotgraph()
        
if __name__ == '__main__':
    main()