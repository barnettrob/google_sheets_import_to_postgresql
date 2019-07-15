# google_sheets_import_to_postgresql
Import Google Sheets rows into a PostgreSQL table

Python script will access the Google Sheet, read it and copy to a PostgreSQL database

https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
https://towardsdatascience.com/accessing-google-spreadsheet-data-using-python-90a5bc214fd2

1. Go to the Google APIs Console.
2. Create a new project.
3. Click Enable API. Search for and enable the Google Drive API.
4. Create credentials for a Web Server to access Application Data.
5. Name the service account and grant it a Project Role of Editor.
6. Enable Google Sheets API by visiting by visiting https://console.developers.google.com/apis/api/sheets.googleapis.com/overview?project=<id>.  If you don't enable this you'll get an error with the correct link with project id to enable it.
6. Download the JSON file.
7. Copy the JSON file to your code directory and rename it to client_secret.json (Not included in repository for security reasons)
8. Also need to activate Google Sheets API
9. Find the client_email inside client_secret.json. Back in your spreadsheet, click the Share button in the top right, and paste the client email into the People field to give it edit rights. Hit Send.

Read Data from a Spreadsheet with Python
oauth2client – to authorize with the Google Drive API using OAuth 2.0
gspread – to interact with Google Spreadsheets

Install these packages with:<br />
`pip install gspread oauth2client`
