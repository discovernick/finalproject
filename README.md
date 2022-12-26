# CS50 Final Project: Sydney Train Game
## Introduction
The Sydney Train Game is a web app inspired by the common game consisiting of making 10 from all the individual carriage numbers on a typical train in Sydney (see below).
Whilst some are easy, it can get real tricky to try and solve this - so I decided to make an app which helps with this. 

The rules of the game are fairly simple:
- You will ignore the letter prefix to the carriage number
- You have to use all 4 digits
- You have to use all digits individually (i.e. if 2010 was the number, you cannot do 20-10=10, instead you have to use 2, 0, 1, 0 individually)
- You can use the standard operations only - addition, subtraction, division and multiplication (once deployed, v2 will include the ability to do power of)

Let's do an example to clarify - 6 8 2 6:
- Step 1: 6 divide 6 equals 1
- Step 2: 2 divide 1 equals 2
- Step 3: 8 plus 2 equals 10 !!!

![Typical Train in Sydney](https://criticalarc.com/wp-content/uploads/2020/11/Sydney_Trains_Trains_W_Logo-1-960x720.jpg)

## Video Overview
https://youtu.be/GzU9kRudGnM

## Deployed Link
*Coming Soon*

I am planning on launching this on Zeet.co for the hosting service and supabase for the database as Heroku (typically used for CS50 Projects) are no longer available to host for free.

## Programming Languages utilised
- Python (Main Programming BackEnd Interface)
- Flask (Framework used to communicate between front-end and back-end)
- SQLite3 (Database Tool)
- HTML (for front-end display - utilising Bootstrap5 components)
- CSS (for styling)
- Javascript (for running Asynchronous Queries using ajax jQuery)

## File Overview
There are three main components to get this up and running. However depending on which database you choose to use, step zero is to establish a database called solutions.db.

Firstly, we run **exportdata.py** which will generate all the solutions for the every digit between 0 - 9999 based on two case scenario's and the four basic operators (+, -, /, *).
This will export to an SQLite 3 Database.

Secondly, we run **combinations.py** which will generate all the unique daily challenges for the next 3850 days from the 20th December 2022, and post them to the database.

Finally, we can run our application in a python environment dictated by the **app.py** file. This file is executed in a flask directory, which contains a templates and static folder. 

The templates folder contains all the individual HTML elements and the static contains the CSS style.


