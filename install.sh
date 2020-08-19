pip3 install virtualenv
virtualenv -p python3 .
source ./bin/activate
pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib
echo "Open https://developers.google.com/drive/api/v3/quickstart/python, Enable Drive API"
echo "In resulting dialog click DOWNLOAD CLIENT CONFIGURATION"
echo "Save the file credentials.json to your working directory"
echo "Now, run run.sh"
