# Sydney Train Game Code

# Import Packages
import os 
from flask import Flask, render_template, flash, jsonify, request
import operator

# Configure Application ( Flask Standard Import Code )
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


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
    stringversion = [int(x) for x in str(inputnumber)]
    stringversion = bubblesort4(stringversion)
    number = stringversion[0]*1000 + stringversion[1]*100 + stringversion[2]*10 + stringversion[3]*1
    return solutions[number]

def interpret(i):
    if i == 'NoSolution':
        return 'No Solution'
    else:
        if i[:2] == 'C1':
            para1 = "( " + i[3] + " " + i[4] + " " + i[5] + " ) = " + str(ops[i[4]](int(i[3]),int(i[5])))
            para2 = "( " + i[7] + " " + i[8] + " " + i[9] + " ) = " + str(ops[i[8]](int(i[7]),int(i[9])))
            para3 = "( " + str(ops[i[4]](int(i[3]),int(i[5]))) + " " + i[6] + " " +str(ops[i[8]](int(i[7]),int(i[9]))) + " ) = " + str(ops[i[6]](ops[i[4]](int(i[3]),int(i[5])), ops[i[8]](int(i[7]),int(i[9]))))
            return para1, para2, para3
        elif i[:2] == 'C2':
            para1 = "( " + i[7] + " " + i[8] + " " + i[9] + " ) = " + str(ops[i[8]](int(i[7]),int(i[9])))
            para2 = "( " + i[5] + " " + i[6] + " " + str(ops[i[8]](int(i[7]),int(i[9]))) + " ) = " + str(ops[i[6]](int(i[5]),int(ops[i[8]](int(i[7]),int(i[9])))))
            para3 = "( " + i[3] + " " + i[4] + " " + str(ops[i[6]](int(i[5]),int(ops[i[8]](int(i[7]),int(i[9]))))) + " ) = " + str(ops[i[4]](int(i[3]),ops[i[6]](int(i[5]),int(ops[i[8]](int(i[7]),int(i[9]))))))
            return para1, para2, para3

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

# Register Page
@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")

# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

# Profile Page
@app.route("/profile", methods=["GET", "POST"])
def profile():
    return render_template("profile.html")

# Solver
@app.route("/solver", methods=["GET", "POST"])
def solver():
    return render_template("solver.html")

# Daily Challenge
@app.route("/daily", methods=["GET", "POST"])
def daily():
    return render_template("daily.html")

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

    # Lookup Solution
    solution = "Solution"
    #para1, para2, para3 = interpret(solution)
    para1 = "Trial 1"
    para2 = "Trial 2"
    para3 = "Trial 3"

    # Create JSON exports
    if (solution == "NoSolution"):
        return jsonify({'NoSolution': 'No Solution' })
    else:
        return jsonify({
            'SolutionH1': 'Solver Solution',
            'Para1' : para1,
            'Para2' : para2,
            'Para3' : para3,
            })