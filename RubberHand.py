#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2023.1.3),
    on November 22, 2023, at 11:54
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
prefs.hardware['audioLib'] = 'ptb'
prefs.hardware['audioLatencyMode'] = '3'
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout
from psychopy.tools import environmenttools
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard



# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2023.1.3'
expName = 'RubberHand'  # from the Builder filename that created this script
expInfo = {
    'participant': f"{randint(0, 999999):06.0f}",
    'session': '001',
}
# --- Show participant info dialog --
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\Brend\\OneDrive\\Documents\\QUT\\2023\\Sem2\\Research Project\\RubberHand.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# --- Setup the Window ---
win = visual.Window(
    size=(1920, 1200), fullscr=True, screen=0, 
    winType='pyglet', allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    backgroundImage='', backgroundFit='none',
    blendMode='avg', useFBO=True, 
    units='height')
win.mouseVisible = False
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess
# --- Setup input devices ---
ioConfig = {}

# Setup iohub keyboard
ioConfig['Keyboard'] = dict(use_keymap='psychopy')

ioSession = '1'
if 'session' in expInfo:
    ioSession = str(expInfo['session'])
ioServer = io.launchHubServer(window=win, **ioConfig)
eyetracker = None

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard(backend='iohub')

# --- Initialize components for Routine "Instructions" ---

# --- Initialize components for Routine "RandomTimer" ---
#From face experiment

# --- Initialize components for Routine "Finger" ---
import time
import serial

PORT = 'COM5'       
BAUD_RATE = 14400     

global hold_time 
# Initialize the serial connection
global ser
ser = serial.Serial(PORT, BAUD_RATE, timeout=10)
time.sleep(2)
ser.flush()


#===========VARIABLES TO PLAY WITH=============
#Finger level Thresholds 
SENSOR_THRESHOLD_MID_UPPER = 510
SENSOR_THRESHOLD_MID_LOW = 490
SENSOR_THRESHOLD_IND_UPPER = 580
SENSOR_THRESHOLD_IND_LOW = 560

#Period to hold finger up for 
hold_time = 1 #[S]

#Servo Angles
#Not Implemented
#==============================================

#ARDUINO READ AND WRITE COMMANDS
def get_sensor_values():
    """
    Function decodes 2 values from serial in form "SENSOR_A, SENSOR_B" and returns as 2 integers
    """
    try:
        read()    
        data = ser.readline().decode('utf-8').strip()
        values = data.split(",")
    except: 
          print("get_sensor_values failed")
    try:
        sensor_values = [int(value) for value in values]
        return sensor_values
    except ValueError:
        return None, None
        
def read_sensor(): 
    """
    Thread streams sensor status from arduino and prints values + updates global variables
    """
    try:
        send_blank()
    except:
        print("Send blank failed")
    mid_sensor, ind_sensor = get_sensor_values()
    if mid_sensor is not None and ind_sensor is not None:
        print("SensorA: ", mid_sensor, "SensorB: ", ind_sensor)
        return mid_sensor, ind_sensor

def read():
        command = 'read\n'
        ser.write(command.encode('utf-8'))
        ser.flush()
        return 1 

#LEFT FINGER COMMANDS
def middle_up():
        command = 'middle_up\n'
        ser.write(command.encode('utf-8'))
        ser.flush()
        return 1

def middle_down():
        print("lowering left")
        command = 'middle_down\n' 
        ser.write(command.encode('utf-8'))
        ser.flush()
        return 1
    
def middle_led_on():
        command = 'middle_led_on\n\n'
        ser.write(command.encode('utf-8'))
        ser.flush()
        return 1

def middle_led_off():
        command = 'middle_led_off\n\n'
        ser.write(command.encode('utf-8'))
        ser.flush()
        return 1

#RIGHT FINGER COMMANDS
def index_up():
        command = 'index_up\n\n'
        ser.write(command.encode('utf-8'))
        ser.flush()
        return 1

def index_down():
        command = 'index_down\n\n' 
        ser.write(command.encode('utf-8'))
        ser.flush()
        return 1
    
def index_led_on():
        command = 'index_led_on\n\n'
        ser.write(command.encode('utf-8'))
        ser.flush()
        return 1

def index_led_off():
        command = 'index_led_off\n\n'
        ser.write(command.encode('utf-8'))
        ser.flush()
        return 1

def send_blank():
        #Send this before reading otherwise arduino can stall waiting for \n before looping
        command = '0\n\n'
        ser.write(command.encode('utf-8'))
        ser.flush()
        return 1

def wait_for_lift():
    """
    Reads Sensor A and B in loop until one exceeds its threshold
    Returns lift_command, lower_command
    """
    print("Wait for lift...")
    while True:
        mid_sensor, index_sensor = read_sensor()
        #Uncomment below to output sensor readings to terminal
        #  print("SensorA: ", mid_sensor, "SensorB: ", ind_sensor)
        #Check if either finger is raised
        if mid_sensor > SENSOR_THRESHOLD_MID_LOW:
            print("Trigger Middle")
            return middle_up, middle_down
        elif index_sensor > SENSOR_THRESHOLD_IND_LOW:
            print("Trigger Index")
            return index_up, index_down

def fingerTrial(finger, condition):
    """
    Loop for lift and lower detection of one finger 
    Input: "middle" or "index" and agree/disagree condition
    """
    print("START TRIAL")

    # Turn on corrosponding LED to indicate the system is active.
    if condition == "Agree":
        if finger == 'middle':
            middle_led_on()
        elif finger == 'index':
            index_led_on()
    elif condition == "Disagree":
        if finger == 'index':
            middle_led_on()
        elif finger == 'middle':
            index_led_on()

    # Wait for either left or right sensor to indicate a finger lift.
    lift_finger, release_finger = wait_for_lift()
    print("LIFTING FINGER...")
    lift_finger()
    time.sleep(hold_time)

    # Turn off the left LED as the action has been detected.
    middle_led_off()
    index_led_off()

    #Wait for the finger to be released.
    print("Checking for release")
    sensorA, sensorB = read_sensor()
    while (sensorA > SENSOR_THRESHOLD_MID_UPPER or sensorB > SENSOR_THRESHOLD_IND_UPPER):
        sensorA, sensorB = read_sensor()

    send_blank()
    release_finger()
    print("Trigger Lower")

# --- Initialize components for Routine "Trust_Slider" ---

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine 

# --- Prepare to start Routine "Instructions" ---
continueRoutine = True
# update component parameters for each repeat
# keep track of which components have finished
InstructionsComponents = []
for thisComponent in InstructionsComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "Instructions" ---
routineForceEnded = not continueRoutine
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
        if eyetracker:
            eyetracker.setConnectionState(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in InstructionsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "Instructions" ---
for thisComponent in InstructionsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "Instructions" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
Blocks = data.TrialHandler(nReps=2.0, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='Blocks')
thisExp.addLoop(Blocks)  # add the loop to the experiment
thisBlock = Blocks.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisBlock.rgb)
if thisBlock != None:
    for paramName in thisBlock:
        exec('{} = thisBlock[paramName]'.format(paramName))

for thisBlock in Blocks:
    currentLoop = Blocks
    # abbreviate parameter names if possible (e.g. rgb = thisBlock.rgb)
    if thisBlock != None:
        for paramName in thisBlock:
            exec('{} = thisBlock[paramName]'.format(paramName))
    
    # set up handler to look after randomisation of conditions etc
    Trials = data.TrialHandler(nReps=3.0, method='random', 
        extraInfo=expInfo, originPath=-1,
        trialList=[None],
        seed=None, name='Trials')
    thisExp.addLoop(Trials)  # add the loop to the experiment
    thisTrial = Trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            exec('{} = thisTrial[paramName]'.format(paramName))
    
    for thisTrial in Trials:
        currentLoop = Trials
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial:
                exec('{} = thisTrial[paramName]'.format(paramName))
        
        # --- Prepare to start Routine "RandomTimer" ---
        continueRoutine = True
        # update component parameters for each repeat
        # keep track of which components have finished
        RandomTimerComponents = []
        for thisComponent in RandomTimerComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "RandomTimer" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
                if eyetracker:
                    eyetracker.setConnectionState(False)
            
            import random
            RandomDelayTimer = random.uniform(1, 3)
            #REMOVE LATER
            time.sleep(RandomDelayTimer)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in RandomTimerComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "RandomTimer" ---
        for thisComponent in RandomTimerComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # the Routine "RandomTimer" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "Finger" ---
        continueRoutine = True
        # update component parameters for each repeat
        # keep track of which components have finished
        FingerComponents = []
        for thisComponent in FingerComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "Finger" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
                if eyetracker:
                    eyetracker.setConnectionState(False)
            
            #GET FINGER FROM EXCEL
            #finger = ...
            if fingerTrial('middle'):
                continueRoutine = False
                
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in FingerComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "Finger" ---
        for thisComponent in FingerComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # the Routine "Finger" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed 3.0 repeats of 'Trials'
    
    
    # --- Prepare to start Routine "Trust_Slider" ---
    continueRoutine = True
    # update component parameters for each repeat
    # keep track of which components have finished
    Trust_SliderComponents = []
    for thisComponent in Trust_SliderComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Trust_Slider" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
            if eyetracker:
                eyetracker.setConnectionState(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Trust_SliderComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Trust_Slider" ---
    for thisComponent in Trust_SliderComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "Trust_Slider" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 2.0 repeats of 'Blocks'


# --- End experiment ---
# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
if eyetracker:
    eyetracker.setConnectionState(False)
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
