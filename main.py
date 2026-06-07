from evdev import ecodes, InputDevice
import evdev
from time import sleep
devices = [InputDevice(_) for _ in evdev.list_devices()]
for _ in devices:
    print(_.path, _.name, _.phys)
print("If you are unable to see your device, try running as root.")
d = input("Event Path (e.g. /dev/input/event0): ")
k = input("Keys to press (e.g: SPACE, A, ENTER. Seperate by `;`): ").upper()
delay = int(input("Delay in ms (1000 - 1s, 3500 - 3.5s): "))


device = InputDevice(d)
keys = k.split(';')

while True:
    try:
         # device.write queues keypresses to the device,
         # device.syn synchroinises keypresse and fires
         # all events that are in queue
         sleep(delay / 1000)
         for k in keys:
            key = getattr(ecodes, f'KEY_{k}')
            for _ in range(2):
                 device.write(ecodes.EV_KEY, key, _-1)
                 device.syn()
                 sleep(0.1)
         # for some reason, some applications will bug
         # if i do not .syn() after down and up
         # they also need a delay, for some reason
         # tested: injustice 2 on wine
         print(f"KeyPress KEY_{k} simulated, CTRL+C to exit.")
    except KeyboardInterrupt:
        print("KeyboardInterrupt, exiting...")
        exit()
