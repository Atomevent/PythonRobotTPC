import evdev
from evdev import InputDevice, categorize, ecodes, KeyEvent
from select import select
import time

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

class Gamepad():
    joyDevice = 0
    last = {
        "ABS_X":0,
        "ABS_Y":0,
        "ABS_RZ": 0,
        "ABS_Z": 0
    }
    def __init__(self):
        self.iDevices = map(evdev.InputDevice, (evdev.list_devices()))
        self.newDevices = {f"{dev.info.vendor}_{dev.info.product}":dev for dev in self.iDevices if dev.path in ['/dev/input/event31']}  
        for keys,values in self.newDevices.items():
            print(keys)
            print(values)
            if(keys=="1133_49689"):
                self.joyDevice = values
        
    def reconnect(self):
        self.iDevices = map(evdev.InputDevice, (evdev.list_devices()))
        self.newDevices = {f"{dev.info.vendor}_{dev.info.product}":dev for dev in self.iDevices if dev.path in ['/dev/input/event31']}  
        for keys,values in self.newDevices.items():
            if(keys=="1133_49689"):
                self.joyDevice = values


if __name__ == "__main__":
    gamePadDevice = Gamepad()
    while gamePadDevice.joyDevice  == 0:
         gamePadDevice.reconnect()
    print(gamePadDevice.joyDevice)
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
                        print('left')
                    elif absevent.event.value == 1:
                        print('right')
                if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_HAT0Y':
                    if absevent.event.value == -1:
                        print('forward')
                    elif absevent.event.value == 1:
                        print('back')
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

