#!/usr/bin/env python
#
#
#******************************************
#******************************************
# Cornell University
# ECE 5725: Web-App based Robot Control(Webo-Pi)
# Authors: ms3368,rs2376
#
#******************************************
#******************************************
#
#

#import the required modules
import os 
import subprocess
import requests
import time
from requests import *
import atexit
from run_test import *
import threading
from flask import Flask,request, redirect,render_template

#Turn the motors off when required
def stop_motors():
    print "Turning motors Off"
    stp()
    
#stop the motors and clean the GPIO before exit.
def at_exit():
    stop_motors()
    GPIO.cleanup()
    
#Register the function to turn the motors off and clean the GPIO at exit.
atexit.register(at_exit)


#move foward
def Foward():
    print "Moving Forward"
    frwrd()
	
#moving backward
def Backward():
    print "Moving Backward"
    bkwrd()
	
#Turn Right
def FowardRight():
    print "Moving Right"
    rgt()

#Turn left
def FowardLeft():
    print "Moving Left"
    lft()

#Increase speed 
def Fast():
    print " Moving Fast"
    Fst()

#Decrease speed
def Slow():
    print "Moving Slow"
    Slw()

#Helper class to store the user related information and about the backend server details.
class UserIdentifier():
    def __init__(self):
	self.user ={}
	self.backend_server_url ="http://0.0.0.0:8082" 	#The static url of the back-end server.
	self.current_user =None			       	#Current user information.
	self.admin_users()			        #Initialize the admin users.
	self.td = threading.Timer(3.0, stop_motors)     #thread to stop the robot after time out

    #function to initialize the admin users
    def admin_users(self):
	self.user['ms3368'] ='3368'
	self.user['rs2376'] ='2376'

#Create instances of the UserIdentifier and the Flask server handler
USERS =UserIdentifier()
USERS.td.start()
app = Flask(__name__)


#function to post the data to the back-end http server.
def do_post_to_server(uname, msg):	
    #Try send the data to the back-end server.
    try:
	#Pack the information to be passed to the back-end http server.
	info_data ={}
	info_data['username'] =uname
	info_data['action'] =msg
	info_data['time'] = time.strftime("%Y-%m-%d %H:%M:%S") #Gather the time information.
	post_response =requests.post(USERS.backend_server_url,data=info_data) #post the info to the back-end http server.
    #Catch the exception when data can't be posted to the http server.
    except:
	pass

#Render the login.html page when the website is hit.
@app.route('/')
def control_screen():
    return render_template('login.html')


#If the login page is refreshed then return the login.html
#else, if the username and password are posted then verify them and proceed accordingly.

@app.route('/login', methods =['POST', 'GET'])
def login():

    if request.method == 'POST':

	#Get the username and password.
    	username =request.form['uname']
    	password =request.form['psw']

	#check if the username is present and if password is correct.
    	if username not in USERS.user.keys() or USERS.user[username] != password:
		err ='Invalid Username or Password !'
		#log the information.
    		output =subprocess.check_output("echo Invalid Login:"+ username +"  >> log_controller.txt", shell=True)

		#post the data to the back-end server.
		do_post_to_server(username, "Invalid Login")

		#Return error on invalid login.
		return render_template('login.html', error=err)
    	else:	
		#log the information.    		
		output =subprocess.check_output("echo "+ username + " Logged In >> log_controller.txt", shell=True)
		#update the current user.
		USERS.current_user =username
		#post the login information to the back-end server.
		do_post_to_server(username, "Logged In")
		#Render the control.html which helps the user control the Robot.
		return render_template('control.html')

    else:
	#Return the same page if refresh button is pressed.
    	return render_template('login.html')


#The control section.
#Based on what button was pressed, control the robot accordingly.

@app.route('/control', methods = ['POST', 'GET'])
def take_action():
    #if the refresh button was pressed then request the user to login for security reasons.
    if request.method == 'GET':
	#Post the log-out information to the back-end http server.
	do_post_to_server(USERS.current_user, "Logged Out")
	return render_template('login.html')

    #Get the information as to what button was pressed.
    button = request.form['button']

    #handling the timeout.
    if USERS.td.is_alive():
        USERS.td.cancel()
        
    USERS.td =threading.Timer(5.0, stop_motors)
    USERS.td.start()
    
    #Log the button press information.
    try:
    	output =subprocess.check_output("echo Action performed " + button + " >> log_controller.txt", shell=True)
    except subprocess.CalledProcessError:
	pass

    #post the button press information to the back-end server.
    do_post_to_server(USERS.current_user, button)

    #Fast button is pressed.
    if button == 'Fast':
        Fast()
    #Slow button is pressed.
    elif button == 'Slow':
        Slow()
    #Forward button is pressed
    elif button == 'Foward':
        Foward()
    #Back button is pressed
    elif button == 'Back':
        Backward()
    #Left button is pressed.
    elif button == 'Left':
        FowardLeft()
    #Right button is pressed.
    elif button == 'Right':
        FowardRight()
    #Stop button is pressed.
    elif button == 'Stop':
        stop_motors()
    #This case will never be hit, kept it for consistency and scalabilty reasons.
    else :
        print("Do Nothing")
    #Return the control.html which contains the control segment
    #every time after the button press to keep the continuity.
    return render_template("control.html")

#Host the web server on port 800, using the flask handle.
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=800 ,debug = True)
