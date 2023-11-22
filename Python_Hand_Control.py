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

#Code for initialising arduino finger angles from python 
# def initialise_angles(angles):
#     command = str(angles[0]) + ", " + str(angles[1])+ ", " + str(angles[2])+ ", " + str(angles[3]) + '\n'
#     print(command)
#     ser.write(command.encode('utf-8'))
#     ser.flush()
#     for i in range(0,1):
#         read_sensor()

# #Example Running
# angles = [90, 90, 90, 90]
# initialise_angles(angles)

fingerTrial('middle')

time.sleep(1)



