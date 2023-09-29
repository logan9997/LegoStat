FILE_NAME = r'C:\Users\logan\OneDrive\Documents\Programming\Python\django\Projects\LegoStat\data_collect\colours.txt'

with open(FILE_NAME, 'r') as file:
    lines = file.readlines()

colours = []
exclude_chars = ['\n', '\t', '?']

for line in lines:
    for char in line:
        if char.isnumeric() or char == ' ' or char == '-':
            line = line.replace(char, '')
    for c in exclude_chars:
        line = line.replace(c, '')
    colours.append(line)

print(colours)