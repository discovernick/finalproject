# Sydney Train Game Code

# Import Packages
import os 
from flask import Flask, render_template, flash, jsonify, request, redirect, session
from flask_session import Session
import operator
import sqlite3
import datetime
from datetime import date
from functools import wraps
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

# Configure Application ( Flask Standard Import Code )
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# From CS50 Finance
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# From CS50 Finance Login Required
def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# Declaring Global Functions
def addZero(inputstring, target):
    if len(inputstring) == target:
        return inputstring
    else:
        inputstring.insert(0,0)
        addZero(inputstring, target)

def init():
    # Get Current Data 
    # Note: Day1 = 20/12/2022
    global tray
    dt1 = datetime.date(2022, 12, 20)
    dt2 = datetime.date.today()
    diff = dt2-dt1
    id = int(diff.days)

    # Get Tray from SQL Server
    con = sqlite3.connect("solutions.db")
    cur = con.cursor()
    cur.execute("SELECT number FROM combinations WHERE id IS ?", (id,))
    daily_number = cur.fetchall()[0][0]

    # Make Tray Elements
    tray = [x for x in str(daily_number)]
    addZero(tray,4)
    return tray

# Initiliase Tray
tray=[]
init()

# Define Operators
ops = {
    '+' : operator.add,
    '-' : operator.sub,
    '*' : operator.mul,
    '/' : operator.truediv,
    '^' : operator.xor,
}

# Define Functions for Execution Code
def solution(inputnumber):
    # Organise numbers
    stringversion = [int(x) for x in str(inputnumber)]
    addZero(stringversion,4)
    print(stringversion)
    stringversion = bubblesort4(stringversion)
    number = stringversion[0]*1000 + stringversion[1]*100 + stringversion[2]*10 + stringversion[3]*1
    print(number)
    # Get Output from SQL Server
    con = sqlite3.connect("solutions.db")
    cur = con.cursor()
    cur.execute("SELECT solutioncode FROM solutions WHERE number IS ?", (number,))
    solution = cur.fetchall()[0][0]
    return solution

def interpret(i):
    if i == 'NoSolution':
        return 'No Solution',"","",""
    else:
        if i[:2] == 'C1':
            para1 = "( " + i[3] + " " + i[4] + " " + i[5] + " ) = " + str(ops[i[4]](int(i[3]),int(i[5])))
            para2 = "( " + i[7] + " " + i[8] + " " + i[9] + " ) = " + str(ops[i[8]](int(i[7]),int(i[9])))
            para3 = "( " + str(ops[i[4]](int(i[3]),int(i[5]))) + " " + i[6] + " " +str(ops[i[8]](int(i[7]),int(i[9]))) + " ) = " + str(ops[i[6]](ops[i[4]](int(i[3]),int(i[5])), ops[i[8]](int(i[7]),int(i[9]))))
            return 'Solution Exists!', para1, para2, para3
        elif i[:2] == 'C2':
            para1 = "( " + i[7] + " " + i[8] + " " + i[9] + " ) = " + str(ops[i[8]](int(i[7]),int(i[9])))
            para2 = "( " + i[5] + " " + i[6] + " " + str(ops[i[8]](int(i[7]),int(i[9]))) + " ) = " + str(ops[i[6]](int(i[5]),int(ops[i[8]](int(i[7]),int(i[9])))))
            para3 = "( " + i[3] + " " + i[4] + " " + str(ops[i[6]](int(i[5]),int(ops[i[8]](int(i[7]),int(i[9]))))) + " ) = " + str(ops[i[4]](int(i[3]),ops[i[6]](int(i[5]),int(ops[i[8]](int(i[7]),int(i[9]))))))
            return 'Solution Exists!', para1, para2, para3

def bubblesort4(arr):
    temp = 0
    for x in range(0,2):
        for y in range(x,2):
            if (arr[y] > arr[y+1]):
                temp = arr[y]
                arr[y] = arr[y+1]
                arr[y+1] = temp
    return arr


# Index Page
@app.route("/")
def home():
    return render_template("index.html")

# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        #Ensure username was submitted
        if not request.form.get("username"):
            print("Username not submitted!")
            return jsonify({
                    'msg' : "Username not submitted!",
            })

        # Ensure password was submitted
        if not request.form.get("password"):
            print("Must provide passowrd")
            return jsonify({
                    'msg' : "Must provide passowrd",
            })

        # Query database for username
        con = sqlite3.connect("solutions.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username IS ?", (request.form.get("username"),) )
        rows = cur.fetchall()
        print(rows[0][2])

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            print("Username doesn't exist")
            return jsonify({
                    'msg' : "Username doesn't exist or passwords dont match!",
            })

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        # Redirect user to home page
        print("made it")
        return render_template("/index.html")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# Register Page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Get Input first
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirmation = request.form.get("password_confirmation")
        print("Username is:" + username)

        # Validate Input
        if (username == "" or password == "" or password_confirmation == ""):
            print("Username, password or confirmation is missing!")
            return jsonify({
                    'msg' : "Username, password or confirmation is missing!",
            })

        if (password != password_confirmation):
            print("Passwords dont match!")
            return jsonify({
                    'msg' : "Passwords dont match!",
            })
        # Validate if user name exists
        con = sqlite3.connect("solutions.db")
        cur = con.cursor()
        existing_users = cur.execute("SELECT username FROM users")
        for dict_element in existing_users:
            print(dict_element[0])
            if (username == dict_element[0]):
                print("That username already exists - Try another!")
                return jsonify({
                        'msg' : "That username already exists - Try another!",
                })

        hash = generate_password_hash(password)
        # Send Output to Database
        cur.execute("INSERT INTO users (username, hash) VALUES(?,?)", (username, hash))
        con.commit()

        # Confirm Registration
        print("got_here")
        return redirect("/login")
    else:
        return render_template("register.html")

# Profile Page
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    # Get username
    con = sqlite3.connect("solutions.db")
    cur = con.cursor()

    id = session.get("user_id")

    cur.execute("SELECT username FROM users WHERE id IS ?", (id,))
    rows = cur.fetchall()
    username = rows[0][0]

    # Get Current Score
    cur.execute("SELECT COUNT(date) FROM history WHERE id IS ?", (id,) )
    score = cur.fetchall()
    print(score[0][0])

    # Get Leaderboard List
    cur.execute("SELECT COUNT(date),username FROM (SELECT * FROM history JOIN users ON history.id = users.id) GROUP BY username  ORDER BY COUNT(date) DESC LIMIT 2")
    leaders = cur.fetchall()
    print(leaders)

    return render_template("profile.html", username=username, leaders=leaders, score=score )


# Solver
@app.route("/solver", methods=["GET", "POST"]) 
def solver():
    return render_template("solver.html")

# Daily Challenge
@app.route("/daily", methods=["GET", "POST"])
@login_required
def daily():
    init()
    return render_template("daily.html", tray=tray)

# AJAX Request for Solver
@app.route('/getsolution', methods=['POST'])
def getsolution():
    # Get Form Data
    numlist = []
    numlist.append(int(request.form.get('N1')))
    numlist.append(int(request.form.get('N2')))
    numlist.append(int(request.form.get('N3')))
    numlist.append(int(request.form.get('N4')))

    # Convert to Single number
    number = 1000*numlist[0]+100*numlist[1]+10*numlist[2]+1*numlist[3]
    print(number)

    # Lookup Solution
    solutioncode = solution(number)
    print(solutioncode)
    h1, para1, para2, para3 = interpret(solutioncode)
    print(para1, para2, para3)
    #para1 = "Trial 1"
    #para2 = "Trial 2"
    #para3 = "Trial 3"

    # Create JSON exports
    if (solution == "NoSolution"):
        return jsonify({
            'h1': h1,
            'Para1' : "",
            'Para2' : "",
            'Para3' : "",
         })
    else:
        return jsonify({
            'h1': h1 ,
            'Para1' : para1,
            'Para2' : para2,
            'Para3' : para3,
            })

# AJAX Request for Daily Challenge
@app.route('/getdaily', methods=['POST'])
def getsdaily():
    init()

    # Get Current Data 
    # Note: Day1 = 20/12/2022
    dt1 = datetime.date(2022, 12, 20)
    dt2 = datetime.date.today()
    diff = dt2-dt1
    id = int(diff.days)
    
    # Lookup SQL server for challenge number
    con = sqlite3.connect("solutions.db")
    cur = con.cursor()
    cur.execute("SELECT number FROM combinations WHERE id IS ?", (id,))
    daily_number = cur.fetchall()[0][0]

    # Make Tray Elements
    daily_tray = [x for x in str(daily_number)]
    addZero(daily_tray,4)

    # Change inner HTML of the number
    return jsonify({
            'number': daily_number ,
            'N1' : daily_tray[0],
            'N2' : daily_tray[1],
            'N3' : daily_tray[2],
            'N4' : daily_tray[3],
    })

# AJAX Request for Tray Submit
@app.route('/traysubmit1', methods=['POST'])
def traysubmit1():
    # Get Current Tray Elements by calling tray

    # Get currently selected values from form
    N1 = request.form.get('N1')
    N2 = request.form.get('N2')
    R1 = request.form.get('R1')
    print(N1,N2,R1)

    # Delete selected elements from tray
    tray.remove(N1)
    tray.remove(N2)
    tray.append(R1)

    return jsonify({
            'N1' : tray[0],
            'N2' : tray[1],
            'N3' : tray[2],
    })

# AJAX Request for Tray Submit
@app.route('/traysubmit2', methods=['POST'])
def traysubmit2():
    # Get Current Tray Elements by calling tray

    # Get currently selected values from form
    N3 = request.form.get('N3')
    N4 = request.form.get('N4')
    R2 = request.form.get('R2')
    print(N3,N4,R2)

    # Delete selected elements from tray
    tray.remove(N3)
    tray.remove(N4)
    tray.append(R2)

    return jsonify({
            'N1' : tray[0],
            'N2' : tray[1],
    })

# AJAX Request for Tray Submit
@app.route('/traysubmit3', methods=['POST'])
def traysubmit3():
    # Get currently selected values from form
    N5 = request.form.get('N5')
    N6 = request.form.get('N6')
    R3 = request.form.get('R3')
    print(N5,N6,R3)

    # Delete selected elements from tray
    tray.remove(N5)
    tray.remove(N6)
    tray.append(R3)

    # Check if person has an entry for todays date, if no add to DB
    if (int(R3) == 10):
        con = sqlite3.connect("solutions.db")
        cur = con.cursor()
        id = session.get("user_id")
        todaysdate = date.today()
        cur.execute("SELECT COUNT(*) FROM history WHERE id IS ? AND date IS ? ", (id, todaysdate) )
        rows = cur.fetchall()
        print(rows[0][0])
        if (int(rows[0][0]) == 0) :
            print("got here!")
            cur.execute("INSERT INTO history (id, date) VALUES(?,?) ", (id, todaysdate) )
            con.commit()

    return jsonify({
            'N1' : tray[0],
    })

# AJAX Request for Tray Revert
@app.route('/trayrevert1', methods=['POST'])
def trayrevert1():
    # Get Current Tray Elements by calling tray

    # Get currently selected values from form
    N1 = request.form.get('N1')
    N2 = request.form.get('N2')
    R1 = request.form.get('R1')

    # Delete selected elements from tray
    tray.append(N1)
    tray.append(N2)
    tray.remove(R1)

    return jsonify({
            'N1' : tray[0],
            'N2' : tray[1],
            'N3' : tray[2],
            'N4' : tray[3],
    })

# AJAX Request for Tray Revert
@app.route('/trayrevert2', methods=['POST'])
def trayrevert2():
    # Get Current Tray Elements by calling tray

    # Get currently selected values from form
    N3 = request.form.get('N3')
    N4 = request.form.get('N4')
    R2 = request.form.get('R2')

    # Delete selected elements from tray
    tray.append(N3)
    tray.append(N4)
    tray.remove(R2)

    return jsonify({
            'N1' : tray[0],
            'N2' : tray[1],
            'N3' : tray[2],
    })

# AJAX Request for Tray Revert
@app.route('/trayrevert3', methods=['POST'])
def trayrevert3():

        # Get Current Tray Elements by calling tray

    # Get currently selected values from form
    N5 = request.form.get('N5')
    N6 = request.form.get('N6')
    R3 = request.form.get('R3')

    # Delete selected elements from tray
    tray.append(N5)
    tray.append(N6)
    tray.remove(R3)

    return jsonify({
            'N1' : tray[0],
            'N2' : tray[1],
    })

# AJAX Request for Current Page 
@app.route('/profile_check', methods=['GET'])
def profile_check():
    # Check if there is an active session
    if len(session) == 0:
        return jsonify ({
            Logged: 'OUT'
        })
    else:
        return jsonify ({
            Logged: 'IN'
        })