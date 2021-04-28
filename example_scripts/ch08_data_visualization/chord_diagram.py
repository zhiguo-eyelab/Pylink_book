#!/usr/bin/env python3
#
# Filename: chord_diagram.py
# Author: Zhiguo Wang
# Date: 4/28/2021
#
# Description:
# A cord diagram to capture the transitions between interest areas

import chord

# The co-occurrence matrix
trans_matrix = [[0, 3, 1, 4, 1],
                [3, 0, 3, 6, 1],
                [1, 3, 0, 9, 1],
                [4, 6, 9, 0, 0],
                [1, 1, 1, 0, 0]]

# Column and row names for the transition matrix
ia_label = ['Brother', 'Mother', 'Father', 'Sister', 'Kite']

# Create a chord diagram and save it to an HTML file
chord.Chord(trans_matrix, ia_label).to_html('transition.html')
