#import geckodriver into your /usr/local/bin
#Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#QR code generator
import pyqrcode
#email recieving/reading
import email
import imaplib
#google sheets
import gspread
from oauth2client.service_account import ServiceAccountCredentials


options = webdriver.FirefoxOptions() #Initializing the webdriver to run headless
options.add_argument('-headless')
 
driver = webdriver.Firefox(firefox_options=options)

driver.get('https://grabify.link/track/SFP9YQ')

#Assigning the official value
spans =[]	
document = driver.find_elements_by_tag_name('span')
for i in document :
    if (i.get_attribute("innerHTML") != "null") :
    	spans.append(i.get_attribute("innerHTML"))
value = spans[34]
spans = [] #Reseting the list
valueplusone = int(value) + 1

#QR code generated
qrurl = pyqrcode.create('https://grabify.link/WXAUYS')
qrurl.svg('textqr.svg', scale=8)
print(qrurl.terminal(quiet_zone=1))
print ("Ready to Scan")

# Waiting for user to scan the qr code it
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

#
#imaplib
#
username = 'xxxx@gmail.com'
password = 'xxxx'

mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(username, password)

mail.select("inbox")
result, data = mail.uid('search', None, 'ALL')
inbox = data[0].split()

#initializes the inbox
computer_inbox = inbox[-1]
user_inbox = inbox[-2]

result, computer_type = mail.uid('fetch', computer_inbox, '(RFC822)')
result, user_type = mail.uid('fetch', user_inbox, '(RFC822)')

raw_user = user_type[0][1]
raw_computer = computer_type[0][1]

user_email = email.message_from_string(raw_user)
computer_email = email.message_from_string(raw_computer)

user_value = user_email['subject']
computer_value = computer_email['subject']

user_value = user_value.split()

name_person = user_value[0] + " " + user_value[1]
grade_school = user_value[2]

		
#google sheets
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('QR-library.json', scope)

gc = gspread.authorize(credentials)

ss = gc.open("Testingspreadsheet")
ws = ss.worksheet("Sheet1")
a1update = ws.update_acell('A2', name_person)
a1update = ws.update_acell('B2', grade_school)
a1update = ws.update_acell('C2', computer_value)