from google.oauth2 import service_account
from googleapiclient.discovery import build
import google.auth


# Replace with your path to the credentials.json file
SERVICE_ACCOUNT_FILE = ''
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']

def get_google_analytics_data():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    analytics = build('analyticsreporting', 'v4', credentials=credentials)
    
    # Replace with your view ID and query parameters
    response = analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': 'YOUR_VIEW_ID',
                    'dateRanges': [{'startDate': '30daysAgo', 'endDate': 'today'}],
                    'metrics': [{'expression': 'ga:sessions'}],
                    'dimensions': [{'name': 'ga:date'}]
                }
            ]
        }
    ).execute()
    
    return response

