import json
import os

sender_list = []

# Prog capture names in message group
def read_mess(file_one):
    data_file = json.load(open(file_one, 'r'))
    for p_name in data_file['participants']:
        add_name = p_name['name']
        if add_name not in sender_list:
            sender_list.append(add_name)
    return sender_list

# Get files first for batch processing
data_files = []
file_list = os.listdir()
for y in file_list:
    if y[-5:] == '.json':
        data_files.append(y)
        
for z in data_files:
    read_mess(z)
