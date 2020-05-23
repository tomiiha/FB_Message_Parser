import json
import os

sender_list = []

# Prog for message set parsing
def read_mess(file_one):
    file_read = open(file_one)
    data_cap = json.load(file_read)
    for x in data_cap['sender_name']:
        sender_list.append(x)
    return  print(sender_list)

# Get files first for batch processing
data_files = []
file_list = os.listdir()
for y in file_list:
    if y[-5:] == '.json':
        data_files.append(y)
