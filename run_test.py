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
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)

#set frequency
freq =46.511
duty_cycle_zerospd =6.976

duty_cycle_maxspd_cw =6.046
duty_cycle_maxspd_acw =7.9069
slow_duty_cycle_cw = 6.700
slow_duty_cycle_acw = 7.076

duty_cycle_cw = slow_duty_cycle_cw
duty_cycle_acw = slow_duty_cycle_acw

right=GPIO.PWM(19,freq)
left=GPIO.PWM(26,freq)
current_command =""

#Update the speed change
def update():
    global current_command
    if current_command == "F":
            frwrd()
    elif current_command == "B":
            bkwrd()
    elif current_command == "L":
            rgt()
    elif current_command == "R":
            lft()

#stop the robot
def stp():
    right.start(0)
    left.start(0)
    current_command =""
    return

#move forward
def frwrd():
    global duty_cycle_cw
    global duty_cycle_acw
    global current_command
    right.start(duty_cycle_acw)
    left.start(duty_cycle_cw)
    current_command ="F"
    return

#move backward
def bkwrd():
    global duty_cycle_cw
    global duty_cycle_acw
    global current_command
    right.start(duty_cycle_cw)
    left.start(duty_cycle_acw)
    current_command ="B"
    return

#turn left
def lft():
    global duty_cycle_cw
    global current_command
    right.start(duty_cycle_cw)
    left.start(duty_cycle_cw)
    current_command ="L"
    return

#turn right
def rgt():
    global duty_cycle_acw
    global current_command
    right.start(duty_cycle_acw)
    left.start(duty_cycle_acw)
    current_command ="R"
    return

#Run Fast, maxlimit speed cannot be changed.
def Fst():
    global duty_cycle_maxspd_cw
    global duty_cycle_maxspd_acw
    global duty_cycle_cw
    global duty_cycle_acw
    duty_cycle_cw = duty_cycle_maxspd_cw
    duty_cycle_acw = duty_cycle_maxspd_acw
    update()
    return

#Run Slow, minlimit is fixed; use stp() to stop the robot.
def Slw():
    global slow_duty_cycle_cw
    global slow_duty_cycle_acw
    global duty_cycle_cw
    global duty_cycle_acw
    duty_cycle_cw = slow_duty_cycle_cw
    duty_cycle_acw = slow_duty_cycle_acw
    update()
    return

    
    
