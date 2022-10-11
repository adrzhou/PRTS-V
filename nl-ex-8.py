import tomli_w


steps = {}

s1 = steps['1'] = {}
s1['x'] = 5
s1['y'] = 1
s1['Operator'] = 'Texas'
s1['Action'] = 'EAST'
s1['Condition'] = 'Sufficient Cost'

s2 = steps['2'] = {}
s2['x'] = 7
s2['y'] = 2
s2['Operator'] = 'Myrtle'
s2['Action'] = 'EAST'
s2['Condition'] = 'Tile Illuminated'

s3 = steps['3'] = {}
s3['x'] = 5
s3['y'] = 1
s3['Operator'] = 'Texas'
s3['Action'] = 'SKILL'
s3['Condition'] = 'Charged'

s4 = steps['4'] = {}
s4['x'] = 8
s4['y'] = 2
s4['Operator'] = 'Ptilopsis'
s4['Action'] = 'WEST'
s4['Condition'] = 'Sufficient Cost'

with open('NL-EX-8.toml', 'wb') as file:
    tomli_w.dump(steps, file)
