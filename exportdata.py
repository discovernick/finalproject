# Import Relevant Packages
from itertools import permutations, product
import operator
import time

# Creating operations combinations
operands = ["+","-","/","*"]

def permSubset(arr, r):
    return list(permutations(arr, r))

def prodSubset(arr, r):
    return list(product(arr, repeat=3))

def bubblesort4(arr):
    temp = 0
    for x in range(0,2):
        for y in range(x,2):
            if (arr[y] > arr[y+1]):
                temp = arr[y]
                arr[y] = arr[y+1]
                arr[y+1] = temp
    return arr

def addZero(inputstring, target):
    if len(inputstring) == target:
        return inputstring
    else:
        inputstring.insert(0,0)
        addZero(inputstring, target)

# Define Operators
ops = {
    '+' : operator.add,
    '-' : operator.sub,
    '*' : operator.mul,
    '/' : operator.truediv,
    '^' : operator.xor,
}

# Main Code

def create_case_both(i):
    # Convert number into digit
    stringversion = [int(x) for x in str(i)]

    # Add Zero's as necessary
    addZero(stringversion, 4)

    # Order the set of numbers - bubble sort
    stringversion = bubblesort4(stringversion)

    # Export rearranged number
    number = stringversion[0]*1000 + stringversion[1]*100 + stringversion[2]*10 + stringversion[3]*1
    
    # Check if the existing number is located within the dictionary
    if number in solutions.keys():
        return

    # Generate sets
    op_com = prodSubset(operands,3)
    num_com = permSubset(stringversion,4)

    # Loop over expressions:
    for i in range(0,len(num_com)):
        for j in range(0,len(op_com)):
            try:
                expression = ops[op_com[j][1]](ops[op_com[j][0]](num_com[i][0],num_com[i][1]), ops[op_com[j][2]](num_com[i][2],num_com[i][3]))
                if expression == 10:
                    solutions[number] = "C1-" + str(num_com[i][0]) + op_com[j][0] + str(num_com[i][1]) + op_com[j][1] + str(num_com[i][2]) + op_com[j][2] + str(num_com[i][3]) 
                    return
            except:
                i=i
        
            try:
                expression = ops[op_com[j][0]](num_com[i][0], ops[op_com[j][1]]( num_com[i][1], ops[op_com[j][2]](num_com[i][2],num_com[i][3])))
                if expression == 10:
                    solutions[number] = "C2-" + str(num_com[i][0]) + op_com[j][0] + str(num_com[i][1]) + op_com[j][1] + str(num_com[i][2]) + op_com[j][2] + str(num_com[i][3]) 
                    return
            except:
                i=i

    solutions[number] = "NoSolution"
    return

# Create Solutions Sandbox
solutions = {}

# Create Dictionary of Solutions
for i in range(0,10000):
    create_case_both(i)