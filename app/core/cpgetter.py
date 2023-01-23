import usb

for dev in usb.core.find(find_all=True):
    a = dev[0][(0,0)][0]
    print((a.bEndpointAddress, a.wMaxPacketSize))

    