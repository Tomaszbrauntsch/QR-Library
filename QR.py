#import geckodriver into your /usr/local/bin
#Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
#QR code generator
import pyqrcode
#email recieving/reading
import email
import imaplib
#google sheets
import gspread
from oauth2client.service_account import ServiceAccountCredentials
print("Starting up...")
#If using Firefox use this | Geckodriver
options = webdriver.FirefoxOptions() #Initializing the webdriver to run headless
options.add_argument('-headless')
driver = webdriver.Firefox(firefox_options=options)

#If using Chromium use this | Chromium driver
'''chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options = chrome_options, executable_path='/usr/bin/chromedriver')
#
'''

#General Information about the usage of the software
print("\nScan the qr code with the name, to remove the entry that matches that name")
print("NOTE: to develop information for the qr codes, the format must be as so:\nmailto:qrtesting1234567890@gmail.com?subject=xxx")
print("Adding info use this format \n1st Code) FirstName LastName Grade \n2nd Code) Computer#")
print("Removing info use this format \n1st Code) FirstName LastName Grade\n")

def addingInfo():
    print("\nAdding an entry into the database")
    print("\nYou may now scan the corresponding QR codes")

    driver.get('https://grabify.link/track/SFP9YQ')

    #Assigning the official value
    spans =[]
    document = driver.find_elements_by_tag_name('span')
    for i in document :
        if (i.get_attribute("innerHTML") != "null") :
        	spans.append(i.get_attribute("innerHTML"))
    value = spans[34]
    spans = [] #Resetting the list
    valueplusone = int(value) + 1

    #QR code generated
    qrurl = pyqrcode.create('https://grabify.link/WXAUYS')
    qrurl.svg('textqr.svg', scale=8)
    print(qrurl.terminal(quiet_zone=1))
    print ("Ready to Scan")

    # Waiting for user to scan the qr code it
    while (int(value) < int(valueplusone)):
    	spans = []
    	document = driver.find_elements_by_tag_name('span')
    	for i in document:
    		if (i.get_attribute("innerHTML") != "null") :
    			spans.append(i.get_attribute("innerHTML"))
    	value = spans[34]
    	driver.refresh()
    print ("Processing...")

    #
    #imaplib protocol being used to access the responses sent by user
    #
    username = 'qrtesting1234567890@gmail.com'
    password = 'testingQR'

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

    credentials = ServiceAccountCredentials.from_json_keyfile_name('qr-library.json', scope)

    gc = gspread.authorize(credentials)

    ss = gc.open("Testingspreadsheet")
    ws = ss.worksheet("Sheet1")
    cell_list = ws.range('A2:A5')
    cell_count = 2

    while (cell_count <= len(cell_list) and ws.acell("A"+str(cell_count)).value != ""):
        cell_count = int(cell_count) + 1
    acellval = "A" + str(cell_count)
    bcellval = "B" + str(cell_count)
    ccellval = "C" + str(cell_count)
    NamecellUpdate = ws.update_acell(acellval, name_person)
    GradecellUpdate = ws.update_acell(bcellval, grade_school)
    ComputercellUpdate = ws.update_acell(ccellval, computer_value)
def removingInfo():
    print("\nRemoving an entry in the database")
    print("\nYou may now scan the corresponding QR codes")

    driver.get('https://grabify.link/track/SFP9YQ')

    #Assigning the official value
    spans =[]
    document = driver.find_elements_by_tag_name('span')
    for i in document :
        if (i.get_attribute("innerHTML") != "null") :
        	spans.append(i.get_attribute("innerHTML"))
    value = spans[34]
    spans = [] #Resetting the list
    valueplusone = int(value) + 1

    #QR code generated
    qrurl = pyqrcode.create('https://grabify.link/WXAUYS')
    qrurl.svg('textqr.svg', scale=8)
    print(qrurl.terminal(quiet_zone=1))
    print ("Ready to Scan")

    # Waiting for user to scan the qr code it
    while (int(value) < int(valueplusone)):
    	spans = []
    	document = driver.find_elements_by_tag_name('span')
    	for i in document:
    		if (i.get_attribute("innerHTML") != "null") :
    			spans.append(i.get_attribute("innerHTML"))
    	value = spans[34]
    	driver.refresh()
    print ("Removing...")

    #
    #imaplib protocol being used to access the responses sent by user
    #
    username = 'qrtesting1234567890@gmail.com'
    password = 'testingQR'

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)

    mail.select("inbox")
    result, data = mail.uid('search', None, 'ALL')
    inbox = data[0].split()

    #gets value from inbox
    user_inbox = inbox[-1]

    result, user_type = mail.uid('fetch', user_inbox, '(RFC822)')
    raw_user = user_type[0][1]
    user_email = email.message_from_string(raw_user)
    user_value = user_email['subject']

    #google sheets
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('qr-library.json', scope)

    gc = gspread.authorize(credentials)

    ss = gc.open("Testingspreadsheet")
    ws = ss.worksheet("Sheet1")
    cell_list = ws.range('A2:A5')
    cell_count = 2

    while (cell_count <= len(cell_list) and ws.acell("A"+str(cell_count)).value != user_value):
        cell_count = int(cell_count) + 1
    acellval = "A" + str(cell_count)
    bcellval = "B" + str(cell_count)
    ccellval = "C" + str(cell_count)
    NamecellUpdate = ws.update_acell(acellval, " ")
    GradecellUpdate = ws.update_acell(bcellval, " ")
    ComputercellUpdate = ws.update_acell(ccellval, " ")

#General Startup
user_input = raw_input("Please enter an (A)DD or (R)emove to add or remove information: ")
while (not(user_input.lower() == "a" or user_input.lower() == "r" or user_input.lower() == "add" or user_input.lower() == "remove")):
    print("An incorrect option was chosen, please enter the correct option")
    user_input = raw_input("Please enter an (A)DD or (R)emove to add or remove information: ")

if (user_input.lower() == "r" or user_input.lower() == "remove"):
    removingInfo()
else:
    addingInfo()
# TODO: Build an UI; Convert to py3
