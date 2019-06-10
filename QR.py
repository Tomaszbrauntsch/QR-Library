#import geckodriver into your /usr/local/bin
#Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#google sheets
import gspread
from oauth2client.service_account import ServiceAccountCredentials
#QR code generator
import pyqrcode

options = webdriver.FirefoxOptions()
options.add_argument('-headless')
 
driver = webdriver.Firefox(firefox_options=options)

driver.get('https://grabify.link/track/SFP9YQ')
spans =[]
document = driver.find_elements_by_tag_name('span')
for i in document :
    if (i.get_attribute("innerHTML") != "null") :
    	spans.append(i.get_attribute("innerHTML"))
value = spans[34]
spans = []
valueplusone = int(value) + 1
print ("Ready to Scan")

#QR code generated
qrurl = pyqrcode.create('https://grabify.link/WXAUYS')
qrurl.svg('textqr.svg', scale=8)
print(qrurl.terminal(quiet_zone=1))

# Waiting for user to scan it
while True:
	spans = []
	document = driver.find_elements_by_tag_name('span')
	for i in document :
		if (i.get_attribute("innerHTML") != "null") :
			spans.append(i.get_attribute("innerHTML"))
	value = spans[34]
	driver.refresh()
	if int(value) == int(valueplusone):
		break
		
#google sheets
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('QR-library.json', scope)

gc = gspread.authorize(credentials)

ss = gc.open("Testingspreadsheet")
ws = ss.worksheet("Sheet1")
a1update = ws.update_acell('A1', 'You scanned the code!')