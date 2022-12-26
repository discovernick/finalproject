# Import Packages
from itertools import product
import random
import sqlite3

# Define generator function
def mixedSubset(arr, r):
    return list(product(arr, repeat=r))

#arr = [x for x in range(0,10)]
#combinations = mixedSubset(arr,4)
#random.shuffle(combinations)
#random.shuffle(combinations)
#random.shuffle(combinations)
#print(combinations)

# Get Output from SQL Server
con = sqlite3.connect("solutions.db")
cur = con.cursor()
cur.execute("SELECT number FROM solutions WHERE NOT solutioncode='NoSolution'")
combinations = cur.fetchall()

# Shufffle three times
random.shuffle(combinations) 
random.shuffle(combinations)
random.shuffle(combinations)

#Update SQL Table
con = sqlite3.connect("solutions.db")
cur = con.cursor()
cur.executemany("INSERT INTO combinations (number) VALUES(?)", combinations)
con.commit() 