#FOR LAUNCH
#export FLASK_APP=app
#export FLASK_RUN_HOST=ipaddress
#flask run --host=192.168.50.189 <- local host
#make sure the count is one to one with the current amount of entities
#https://stackoverflow.com/questions/24892035/how-can-i-get-the-named-parameters-from-a-url-using-flask
#
#find amount of cells
#
from flask import Flask, request, session
#google sheets
import gspread
from oauth2client.service_account import ServiceAccountCredentials
app = Flask(__name__)
app.secret_key="abc" #needed to use session[]

#fix hosting ip app.run
#http://127.0.0.1:5000/input?fname=joe&lname=mama
#http://127.0.0.1:5000/input?cname=computer001
#http://127.0.0.1:5000/done
#192.168.50.100
@app.route('/')
def home_page():
    return 'nothing here'

@app.route('/input')
def reading_vals():
    #session is used to pass values between routes
    if (str(request.args.get('fname')) != "None"):
        session['fName'] = str(request.args.get('fname'))
    if (str(request.args.get('lname')) != "None"):
        session['lName'] = str(request.args.get('lname'))
    if (str(request.args.get('cname')) != "None"):
        session['cName'] = str(request.args.get('cname'))
    return ('Entry Submitted')

#http://127.0.0.1:5000/addInfo
@app.route('/addInfo')
def add():
    fName = str(session.get('fName'))
    lName = str(session.get('lName'))
    cName = str(session.get('cName'))
    print("This is the done section")
    delete = False
    googlesheets(fName, lName, cName, delete)
    return "Info was Added"

#http://127.0.0.1:5000/removeInfo
@app.route('/removeInfo')
def remove():
    fName = str(session.get('fName'))
    lName = str(session.get('lName'))
    cName = str(session.get('cName'))
    print("This is the done section")
    delete = True
    googlesheets(fName, lName, cName, delete)
    return "Info was removed"

def googlesheets(fName, lName, cName, delete):

        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']

        credentials = ServiceAccountCredentials.from_json_keyfile_name('QR-Library.json', scope)

        gc = gspread.authorize(credentials)
        ws = gc.open("Database").sheet1
        cell_count = ws.acell("D1").value #start
        if delete == False:
            ws.update_acell(("A" + str(cell_count)), fName)
            ws.update_acell("B" + str(cell_count), lName)
            ws.update_acell("C" + str(cell_count), cName)
            ws.update_acell("D1", str(int(cell_count) + 1)) #updates to the first avaliable blank cell
        else:
            temp_cell = 2 #first name on the list
            searchC = ws.acell("C" + str(temp_cell)).value #compName value at C[x] in DB
            while(cName != searchC):
                #looks if user-entry is found, to remove the correct entry
                temp_cell += 1
                searchC = ws.acell("C" + str(temp_cell)).value #compName value at C[x] in DB
            #moves all entries up to fill in blank
            for x in range(temp_cell, (int(cell_count) + 1)): #start, end
                ws.update_acell("A" + str(x), ws.acell("A" + str(x + 1)).value)
                ws.update_acell("B" + str(x), ws.acell("B" + str(x + 1)).value)
                ws.update_acell("C" + str(x), ws.acell("C" + str(x + 1)).value)
            ws.update_acell("D1", str(int(cell_count) - 1)) #updates next avaliable blank cell
