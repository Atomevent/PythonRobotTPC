from smbus2 import SMBus
from external.joyObj import Gamepad
import time
import evdev
from evdev import InputDevice, categorize, ecodes, KeyEvent
from select import select

motorDrives = {"Left":0x50,
               "Right":0x51}
maxMotorSpeed = 255
codeToButtonDict = {"BTN_X":304,
                    "BTN_A":305,
                    "BTN_B":306,
                    "BTN_Y":307,
                    "BTN_LB":308,
                    "BTN_RB":309,
                    "BTN_LT":310,
                    "BTN_RT":311,
                    "BTN_BACK":312,
                    "BTN_START":313,
                    "BTN_L3":314,
                    "BTN_R3":315}
def handleJoystick():
    pass
def forward(speed):
    print("Hi")
    pass
def backward(speed):
    pass
def slideLeft(speed):
    pass 
def slideRight(speed):
    pass
def main():
    SMBus1 = SMBus(1)
    gamePadDevice = Gamepad()
    while gamePadDevice.joyDevice  == 0:
        gamePadDevice.reconnect()
    gamePadDevice = Gamepad()
    for event in gamePadDevice.joyDevice.read_loop():      
        if event.type == ecodes.EV_KEY:
                keyevent = categorize(event)
                print(type(event.code))
                if keyevent.keystate == KeyEvent.key_down:
                        if event.code == codeToButtonDict["BTN_A"]:
                              print("Hi")
                                
        elif event.type == ecodes.EV_ABS:
                absevent = categorize(event)
                if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_HAT0X':
                    if absevent.event.value == -1:
                        slideLeft(maxMotorSpeed)
                    elif absevent.event.value == 1:
                        slideRight(maxMotorSpeed)
                if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_HAT0Y':
                    if absevent.event.value == -1:
                        forward(maxMotorSpeed)
                    elif absevent.event.value == 1:
                        backward(maxMotorSpeed)
                if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_X':
                    gamePadDevice.last["ABS_X"] = absevent.event.value -128
                if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_Y':
                    gamePadDevice.last["ABS_Y"] = absevent.event.value -128
                if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_Z':
                    gamePadDevice.last["ABS_Z"] = absevent.event.value -128
                if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_RZ':
                    gamePadDevice.last["ABS_RZ"] = absevent.event.value -128
                if(abs(gamePadDevice.last["ABS_X"])<5):
                    gamePadDevice.last["ABS_X"] = 0
                if(abs(gamePadDevice.last["ABS_Y"])<5):
                    gamePadDevice.last["ABS_Y"] = 0
                if(abs(gamePadDevice.last["ABS_Z"])<5):
                    gamePadDevice.last["ABS_Z"] = 0
                if(abs(gamePadDevice.last["ABS_RZ"])<5):
                    gamePadDevice.last["ABS_RZ"] = 0
                print(gamePadDevice.last)
        handleJoystick()


main()