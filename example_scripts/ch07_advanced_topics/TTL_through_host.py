# Filename: TTL_through_host.py
# Author: Zhiguo Wang
# Date: 11/7/2020
#
# Description:
# Send TTL through the EyeLink Host PC
# Here we assume an EyeLink 1000 Plus tracker is being tested. The
# base address is 0x8, and address for the Control Register is 0xA
# for EyeLink 1000, the base address is 0x378, address for the Control
# Register is 0x37A; for Portable DUO and laptop Hosts with
# the USB2TTL8 adapter, the base address is 0x7

import pylink

# Connect to the tracker
tk = pylink.EyeLink('100.1.1.1')

# Open and EDF data file on the Host
tk.openDataFile('ttl_test.edf')

# Start recording
tk.startRecording(1, 1, 1, 1)

# Make sure the Bi-Directional mode is off on the Host
tk.writeIOPort(0xA, 0)

# Using the Pylink function writeIOPort to send TTLs

# Clear the Data Register
tk.writeIOPort(0x8, 0)
pylink.pumpDelay(100)

# Send 8 TTL signals through the Host
for i in range(201, 209):
    # Write a TTL the Data Register
    tk.writeIOPort(0x8, i)
    # TTL signal duration--20 ms
    pylink.pumpDelay(20)
    # Clear the Data Register
    tk.writeIOPort(0x8, 0)
    pylink.pumpDelay(1000)

# Using the Host command'write_ioport' command to send TTLs
# The "*" in the command request the Host to log the command
# the EDF data file

# Clear the Data Register
tk.sendCommand('write_ioport 0x8 0')
pylink.pumpDelay(100)

# Send 8 TTL signals through the Host
for i in range(1, 9):
    # Write a TTL the Data Register
    tk.sendCommand('*write_ioport 0x8 %d' % i)
    # TTL signal duration--20 ms
    pylink.pumpDelay(20)
    # Clear the Data Register
    tk.sendCommand('write_ioport 0x8 0')
    pylink.pumpDelay(1000)

# Stop recording
tk.stopRecording()

# Close the EDF data file and download it from the Host
tk.closeDataFile()
tk.receiveDataFile('ttl_test.edf', 'ttl_test.edf')

# Close the link to the tracker
tk.close()
