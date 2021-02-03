#! /usr/bin/env python3
#
# Filename: file_operation.py
# Author: Zhiguo Wang
# Date: 2/3/2020
#
# Description:
# Open, read, and write plain text files

file_name = 'file_op.txt'
# Open a file with 'write' permission,
# Write three lines of texts into the file, then
# close the file
print('Wring three lines of text to %s' % file_name)
file = open(file_name, 'w')
for i in range(3):
    file.write('This is line %d\n' % (i+1))
file.close()

# Open a file, read the first line with the
# readline() method, then close the file
print('\n\nRead the first line in %s' % file_name)
file = open('file_op.txt', 'r')
line = file.readline()
print(line)
file.close()

# Open a file with 'read' permission,
# read 4 characters, then close the file
print('\n\nRead the first four characters in %s' % file_name)
file = open('file_op.txt', 'r')
txt = file.read(4)
print(txt)
file.close()

# Open a file, loop over all lines, then
# close the file
print('\n\nRead all lines in %s' % file_name)
file = open('file_op.txt', 'r')
for line in file:
    print(line)
file.close()

# Use a "with" statement, so the file is properly
# closed following the file operations
print('\n\nRead all lines using a with-statement')
with open('file_op.txt', 'r') as file:
    for line in file:
        print(line.rstrip())
