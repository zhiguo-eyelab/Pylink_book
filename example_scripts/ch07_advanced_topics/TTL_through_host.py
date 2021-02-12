#!/usr/bin/env python3
#
# Filename: TTL_through_host.py
# Author: Zhiguo Wang
# Date: 2/5/2021
#
# Description:
# Send TTL through the EyeLink Host PC
# Here we assume an EyeLink 1000 Plus tracker is being tested. The
# base address is 0x8, and address for the Control Register is 0xA
# for EyeLink 1000, the base address is 0x378, address for the Control
# Register is 0x37A

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

for i in range(201, 209):
    # Write a TTL to the Data Register
    tk.writeIOPort(0x8, i)
    # TTL signal duration--20 ms
    pylink.pumpDelay(20)
    # Clear the Data Register
    tk.writeIOPort(0x8, 0)
    # Wait for 1 second before we send the next TTL
    pylink.pumpDelay(1000)

# Using the Host 'write_ioport' command to send TTLs
# The "*" in the command request the Host to log the command in
# the EDF data file

# Clear the Data Register
tk.sendCommand('write_ioport 0x8 0')
pylink.pumpDelay(100)

for j in range(1, 9):
    # Write a TTL to the Data Register
    tk.sendCommand(f'*write_ioport 0x8 {j}')
    # TTL signal duration--20 ms
    pylink.pumpDelay(20)
    # Clear the Data Register
    tk.sendCommand('write_ioport 0x8 0')
    # Wait for 1 second before we send the next TTL
    pylink.pumpDelay(1000)

# Stop recording
tk.stopRecording()

# Close the EDF data file and download it from the Host PC
tk.closeDataFile()
tk.receiveDataFile('ttl_test.edf', 'ttl_test.edf')

# Close the link to the tracker
tk.close()
