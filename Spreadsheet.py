import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('QR-library.json', scope)

gc = gspread.authorize(credentials)

ss = gc.open("Testingspreadsheet")
ws = ss.worksheet("Sheet1")
val = ws.acell('A1').value
print(val)
a1update = ws.update_acell('A1', 'BYE THERE!'')
val = ws.acell('A1').value
print(val)
