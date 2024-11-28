import os
import re
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from requests import Request
from google.auth.transport.requests import Request

print()
# If modifying the API, set SCOPES
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail_api():
    """Authenticate and return the Gmail API service."""
    creds = None
    print("--------------------------------------------------")

    # The file token.json stores the user's access and refresh tokens.
    # It is created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def get_last_email_from_sender(service, sender_email):
    """Get the last email from a specific sender."""
    try:
        # List messages from the sender
        query = f'from:{sender_email}'
        results = service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])

        if not messages:
            print(f'No messages found from {sender_email}.')
            return None
        
        # Get the most recent message
        message_id = messages[0]['id']
        message = service.users().messages().get(userId='me', id=message_id).execute()

        # Get the email content
        snippet = message['snippet']
        print(f'Last email from {sender_email}:')
        print("message : ",snippet)
        return snippet

    except HttpError as error:
        print(f'An error occurred: {error}')
        return None
    

def extract_otp(snippet):
    """Extract the OTP from the email snippet using regex."""
    # Regex pattern for a 6-digit number
    otp_pattern = r'\b\d{6}\b'
    match = re.search(otp_pattern, snippet)
    if match:
        return match.group(0)
    return None

def otp_get_from():
    service = authenticate_gmail_api()
    print(service,"wwwwwwwwwwwwwww")
    sender_email = 'noreply@donotreply.acct-mgmt.com'
    last_email = get_last_email_from_sender(service, sender_email)
    otp =  extract_otp(last_email)
    if last_email:
        return otp
    else:
        return 000000
        # print('Email Snippet:', otp)

    

# if __name__ == '__main__':
#     otp = otp_get_from()
#     print(otp)
