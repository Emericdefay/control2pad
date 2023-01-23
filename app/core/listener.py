#!/usr/bin/python
import sys
import usb.core
import usb.util

import os.path, sys
sys.path.append(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
)

from layouts import cpManager
from mapping import MAP
from settings import core_settings

set_endpoints = set()

for dev in usb.core.find(find_all=True):
    endpoint = dev[0][(0,0)][0]
    set_endpoints.add(endpoint)

# decimal vendor and product values
# or, uncomment the next line to search instead by the hexidecimal equivalent
dev = usb.core.find(idVendor=0x2516, idProduct=0x7b)

dev.set_configuration()
# first endpoint
interface = 0

try:
    endpoint = dev[0][(0,0)][0]
except TypeError as e:
    # print("ERROR : Controlpad not found.")
    raise ConnectionError('ControlPad not found')


# if the OS kernel already claimed the device, which is most likely true : 
try:
    if dev.is_kernel_driver_active(interface) is True:
        # tell the kernel to detach
        dev.detach_kernel_driver(interface)
        # claim the device
        usb.util.claim_interface(dev, interface)
except Exception as e:
    if core_settings.DEBUG:
        print('WARNING : "is_kernel_driver_active" function not able on Windows')
    pass

KEYS = cpManager.get_cp_keys()
collected = 0
attempts = 50_000
# while collected < attempts :
while True :
    try:
        data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
        collected += 1
        # print(data)
        if data in KEYS.values():
            index = list(KEYS.values()).index(data)
            key = list(KEYS.keys())[index]
            if core_settings.DEBUG:
                print(key)
            MAP.get(key)()
    except usb.core.USBError as e:
        data = None
        if e.args == ('Operation timed out',):
            continue
    except Exception as e:
        print(e)
        break
# release the device
usb.util.release_interface(dev, interface)
try:
    # reattach the device to the OS kernel
    dev.attach_kernel_driver(interface)
except Exception as e:
    print('WARNING : "attach_kernel_driver" function not able on Windows')
    pass
