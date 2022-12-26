# CS50 Final Project: Sydney Train Game
## Introduction
The Sydney Train Game is a web app inspired by the common game consisiting of making 10 from all the individual carriage numbers on a typical train in Sydney (see below).
Whilst some are easy, it can get real tricky to try and solve this - so I decided to make an app which helps with this.

![Typical Train in Sydney](https://criticalarc.com/wp-content/uploads/2020/11/Sydney_Trains_Trains_W_Logo-1-960x720.jpg)

## Video Overview
https://youtu.be/GzU9kRudGnM

## Deployed Link
*Coming Soon*

## Programming Languages utilised
- Python 
- Flask 
- SQLite3
- HTML
- CSS
- Javascript

## File Overview
There are three main components to get this up and running.

Firstly, we run **exportdata.py** which will generate all the solutions for the every digit between 0 - 9999 based on two case scenario's and the four basic operators (+, -, /, *).
This will export to an SQLite 3 Database.

Secondly, we run **combinations.py** which will generate all the unique daily challenges for the next 3850 days from the 20th December 2022, and post them to the database.

Finally, we can run our application in a python environment dictated by the **app.py** file.


