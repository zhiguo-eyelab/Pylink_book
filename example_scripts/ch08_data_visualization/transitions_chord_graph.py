# Filename: transitions_chord_graph.py

import chord

# the fas transition matrix
fsa_duration =[[4109, 464,  724,  511, 365],
               [3046, 617,  578,  507,  147],
               [0,    1691, 2269, 581,  0],
               [75,   269,  646,  2359, 0],
               [0,    143,  0,    200,  240]]

# the interest area labels (column and row labels for the
# above transition matrix
ia_label = ['Brother', 'Mother', 'Father', 'Sister', 'Kite']

# create a chord graph and save it as a HTML file
chord.Chord(fsa_duration, ia_label).to_html('flying_kite.html')
