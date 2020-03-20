# Filename: TTL_through_host.py

# Here we assume an EyeLink 1000 Plus tracker is being tested
# for EyeLink 1000, the base address is 0x378, address for Control
# register is 0x37A; for Portable DUO and laptop Hosts with
# the USB2TTL8 adapter, the base address is 0x7 and the address for the
# Control Register is 0x9

import pylink

# connect to the tracker
tk = pylink.EyeLink('100.1.1.1')

tk.openDataFile('ttl_test.edf')
tk.startRecording(1,1,1,1)

# make sure Bi-Directional mode is off on the Host
tk.writeIOPort(0xA, 0)

# using the Pylink function writeIOPort to send a TTL
tk.writeIOPort(0x8, 0) # clear the Data Register
pylink.pumpDelay(100)
for i in range(201,209):
    tk.writeIOPort(0x8, i)
    pylink.pumpDelay(10)
    tk.writeIOPort(0x8, 0)
    pylink.pumpDelay(100)

#using the Host command'write_ioport' command and command execution time
tk.sendCommand('*write_ioport 0x8 0') # clear the Data Register
pylink.pumpDelay(100) 
for i in range(1,9):
    tk.sendCommand('*write_ioport 0x8 %d' %i)
    pylink.pumpDelay(10)
    tk.sendCommand('*write_ioport 0x8 0')
    pylink.pumpDelay(1000)

tk.stopRecording()
tk.closeDataFile()
tk.receiveDataFile('ttl_test.edf', 'ttl_test.edf')

# close the link to the tracker
tk.close()
