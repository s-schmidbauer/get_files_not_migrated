# Perform steps in INSTALL
# https://developers.google.com/drive/api/v3/quickstart/python, Enable Drive API
# In resulting dialog click DOWNLOAD CLIENT CONFIGURATION 
# Save the file credentials.json to your working directory.

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def main():
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

    drive_service = build('drive', 'v3', credentials=creds)

    # Script starts here
    page_token = None

    # Find folders containing our domain (after exported to user from Admin Console)
    folders = drive_service.files().list(q="name contains '@abbywinters.com' and mimeType='application/vnd.google-apps.folder'",
                                          spaces='drive',
                                          fields='nextPageToken, files(id, name)',
                                          pageToken=page_token).execute()

    #Print message about count of folders found
    print("%s folders found to be cleaned up." % (len(folders.get('files', []))))

    # For all folders found, find files within folder
    for folder in folders.get('files', []):
        folder_id = folder.get('id')
        folder_files = drive_service.files().list(q="'{}' in parents and mimeType != 'application/vnd.google-apps.folder'".format(folder_id),
                                                  spaces='drive',
                                                  fields='nextPageToken, files(id, name)',
                                                  pageToken=page_token).execute()

        # Count all files within the folder
        count = 0
        for file in folder_files.get('files', []):
	    #Print file name if necessary
    	    #print("%s" % (file.get('name')))
    	    count += 1

        # Do something with that
        if count > 0:
            print("%s with %s file(s)" % (folder.get('name'), count))

        if count == 0:
            print("%s with 0 files" % (folder.get('name')))

if __name__ == '__main__':
    main()
