import sys, ftd2xx as ftd
import time
d = ftd.open(0)    # Open first FTDI device
print(d.getDeviceInfo())

OP = 0x01            # Bit mask for output D0
d.setBitMode(OP, 1)  # Set pin as output, and async bitbang mode
d.write(str(OP))     # Set output high
time.sleep(1)
d.write(str(0))      # Set output low