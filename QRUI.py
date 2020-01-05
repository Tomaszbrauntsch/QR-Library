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
#ui building
import Tkinter as tk
from Tkinter import *
#threading
import threading
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

#addinfo-window
def addInfo_window():
        top = Toplevel()
        top.title('Adding an entry to database')
        top.config(bg="#1dd4f0")
        labeltext = StringVar()
        label = tk.Label(top, textvariable=labeltext, width="50", height="10", font="none, 16", bg="#1dd4f0").pack()
        labeltext.set("Adding an entry to the Database...\n\nYou may now also scan the corresponding QR codes\n")
        #goBackButton = tk.Button(top, text="Go back to home page", width=25, bg="white", fg="black", activebackground="#000000", activeforeground="#FFF", command=top.destroy).pack()

        def addInfo():
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
            qrurl.svg('qrcode.svg', scale=8)
             #update label
            labeltext.set("Scan the QR code on screen to continue...")
            canvas = Canvas(top, width=375, height=400, bg="#1dd4f0", bd=0, highlightthickness=0)
            canvas.pack()
            img = PhotoImage(file="qrcode.png")
            canvas.create_image(20,20, anchor=NW, image=img)

            #Waiting for user to scan the qr code
            while (int(value) < int(valueplusone)):
            	spans = []
            	document = driver.find_elements_by_tag_name('span')
            	for i in document:
            		if (i.get_attribute("innerHTML") != "null") :
            			spans.append(i.get_attribute("innerHTML"))
            	value = spans[34]
            	driver.refresh()
            labeltext.set("Processing your request...") #update label

            print("request is being processed")

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
            cell_list = ws.range('A2:A20')
            cell_count = 2

            while (cell_count <= len(cell_list) and ws.acell("A"+str(cell_count)).value != ""):
                cell_count = int(cell_count) + 1
            acellval = "A" + str(cell_count)
            bcellval = "B" + str(cell_count)
            ccellval = "C" + str(cell_count)
            NamecellUpdate = ws.update_acell(acellval, name_person)
            GradecellUpdate = ws.update_acell(bcellval, grade_school)
            ComputercellUpdate = ws.update_acell(ccellval, computer_value)
            top.destroy()

        addThread = threading.Thread(target=addInfo)
        addThread.start()

def removeInfo_window():
        top = Toplevel()
        top.title('Removing an entry from database')
        top.config(bg="#eb6d07")
        labeltext = StringVar()
        label = tk.Label(top, textvariable=labeltext, width="50", height="10", font="none, 16", bg="#eb6d07", fg="white")
        labeltext.set("Removing an entry to the Database...\n\nYou may now scan the corresponding QR code\n")
        label.pack()

        def removeInfo():
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
            qrurl.svg('qrcode.svg', scale=8)
             #update label
            labeltext.set("Scan the QR code on screen to continue...")
            canvas = Canvas(top, width=375, height=400, bg="#eb6d07", bd=0, highlightthickness=0)
            canvas.pack()
            img = PhotoImage(file="qrcode.png")
            canvas.create_image(20,20, anchor=NW, image=img)

            #Waiting for user to scan the qr code
            while (int(value) < int(valueplusone)):
            	spans = []
            	document = driver.find_elements_by_tag_name('span')
            	for i in document:
            		if (i.get_attribute("innerHTML") != "null") :
            			spans.append(i.get_attribute("innerHTML"))
            	value = spans[34]
            	driver.refresh()
            labeltext.set("Removing your requested entry...") #update label

            print("request is being processed")

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
            cell_list = ws.range('A2:A20')
            cell_count = 2

            while (cell_count <= len(cell_list) and ws.acell("A"+str(cell_count)).value != user_value):
                cell_count = int(cell_count) + 1
            acellval = "A" + str(cell_count)
            bcellval = "B" + str(cell_count)
            ccellval = "C" + str(cell_count)
            NamecellUpdate = ws.update_acell(acellval, " ")
            GradecellUpdate = ws.update_acell(bcellval, " ")
            ComputercellUpdate = ws.update_acell(ccellval, " ")
            top.destroy()

        removeThread = threading.Thread(target=removeInfo)
        removeThread.start()

#
#Main window
#
app = tk.Tk()
app.config(bg="#1dd4f0")
app.title("Home Page")
textforLabel = "Welcome to the QR-Library Database\n\nClick on one of the options to continue\nInstructions:\nScan the qr code with the name, to remove the entry that matches that name\n"
textforLabel = textforLabel + "NOTE: to develop information for the qr codes, the format must be as so:\nmailto:qrtesting1234567890@gmail.com?subject=xxx\n"
textforLabel = textforLabel + "\nAdding info use this format: \n1st Code) FirstName LastName Grade \n2nd Code) Computer#\n\nRemoving info use this format: \n1st Code) FirstName LastName Grade\n"
textforLabel = textforLabel + "IMPORTANT: DO NOT CLOSE THE WINDOW WHILE YOU ARE IN THE MIDDLE OF PROCESSING, \nYOU WILL HAVE TO START OVER"
labelText = Label(app, text=textforLabel, width="75", height="20", font="none, 16", bg="#eb6d07")


addInfoButton = tk.Button(app, text="Add Information", width=25, bg="white", fg="black", activebackground="#000000", activeforeground="#FFF", bd=0, highlightthickness=2, highlightbackground="black", command=addInfo_window)
removeInfoButton = tk.Button(app, text="Remove Information", width=25, bg="white", fg="black", activebackground="#000000", activeforeground="#FFF", bd=0, highlightthickness=2, highlightbackground="black", command=removeInfo_window)
quitButton = tk.Button(app, text="Quit App", width=25, bg="white", fg="black", activebackground="#000000", activeforeground="#FFF", bd=0, highlightthickness=2, highlightbackground="black", command=app.destroy)

labelText.pack()
addInfoButton.pack()
removeInfoButton.pack()
quitButton.pack()

app.mainloop()
