import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('QR-library.json', scope)

gc = gspread.authorize(credentials)

ss = gc.open("Testingspreadsheet")
ws = ss.worksheet("Sheet1")
cell_count = 2
cell_list = ws.range('A1:A5')
for i in cell_list:
   cell_value = "A" + str(cell_count)
   if ws.acell(cell_value).value == "":
      print (cell_value)
   cell_count = int(cell_count) + 1


#val = ws.acell('A1').value
#a1update = ws.update_acell('A1', 'BYE THERE!'')
#val = ws.acell('A1').value
