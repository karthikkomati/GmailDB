from __future__ import print_function
from mysql import connector
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import configparser


config = configparser.ConfigParser()
config.read('config.ini')


mydb = connector.connect(
  host = config["GmailDatabase"]['Host'],
  user = config["GmailDatabase"]['User'],
  password = config["GmailDatabase"]['Password'],
  database  = config["GmailDatabase"]['Database']
)

# mycursor = mydb.cursor()
        
# sql1 = 'TRUNCATE TABLE maildata'           

# mycursor.execute(sql1)
# mydb.commit()



no_of_emails = 5



SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
creds = None

if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

    with open('token.json', 'w') as token:
        token.write(creds.to_json())

service = build('gmail', 'v1', credentials=creds)

    
results = service.users().messages().list(userId='me').execute()


labels = results.get('messages', [])

if not labels:
    print('No labels found.')
else:
    #print('Labels:')
    i = 1
    for label in labels:
        
        re = service.users().messages().get(userId='me',id=label['id']).execute()
        
        mail_id = re['id']
        thread_id = re['threadId']
        snippet = re['snippet']
        
        #print(type(mail_id))
        #print(type(thread_id))

        
        
        try:
            mycursor = mydb.cursor()
            
            sql = 'INSERT INTO maildata (ID,ThreadID,MailSnippet) VALUES ("{}","{}","{}")'.format(mail_id,thread_id,snippet)
            
            #print(sql)
            mycursor.execute(sql)
            mydb.commit()
        except connector.errors.IntegrityError as e:
            print(e)
        
        #print("---------------------------------------------")
        if i>=no_of_emails:
            break
        i+=1