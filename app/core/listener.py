#!/usr/bin/python
import sys
import usb.core
import usb.util

import os.path, sys
sys.path.append(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
)

from PyQt5.QtCore import (
    Qt,
    QThread,
    pyqtSlot,
    pyqtSignal,
)

from layouts import cpManager
from mapping import MAP
from settings import core_settings
from settings.json_settings import load_settings

from widgets.cpshower import KeyButton


def listen_usb(idVendor, idProduct, keyboard_map):
    set_endpoints = set()

    for dev in usb.core.find(find_all=True):
        endpoint = dev[0][(0,0)][0]
        set_endpoints.add(endpoint)

    # decimal vendor and product values
    # or, uncomment the next line to search instead by the hexidecimal equivalent
    dev = usb.core.find(idVendor=idVendor, idProduct=idProduct)

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

    KEYS = cpManager.get_cp_keys(idVendor,idProduct)
    keys_values = list(KEYS.values())
    keys_keys = list(KEYS.keys())
    # while collected < attempts :

    keys_obj_list = keyboard_map.get_keys_list()
    keys_obj_dict = {k.key_name: k for k in keys_obj_list}

    while not keyboard_map.stopped:
        try:
            data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
            # print(data)
            if data in keys_values:
                index = keys_values.index(data)
                key = keys_keys[index]
                if core_settings.DEBUG:
                    print(key)
                # MAP.get(key)()
                if key in keys_obj_dict:
                    keys_obj_dict[key].on_key_pressed()
                
        except usb.core.USBError as e:
            data = None
            if e.args == ('Operation timed out',):
                continue
        except Exception as e:
            print(e)
            break
    print("leave listener")
    # release the device
    usb.util.release_interface(dev, interface)
    try:
        # reattach the device to the OS kernel
        dev.attach_kernel_driver(interface)
    except Exception as e:
        print('WARNING : "attach_kernel_driver" function not able on Windows')
        pass


if __name__ == '__main__':
    settings =  load_settings()
    _cpVID = settings.get('VID', 0x2516)
    _cpPID = settings.get('PID', 0x007B)
    listen_usb(idVendor=_cpVID, idProduct=_cpPID)