import json
import os

sender_list = []
data_files = []
results = {}

# Get files first for batch processing
file_list = os.listdir()
for y in file_list:
    if y[-5:] == '.json':
        data_files.append(y)

# Prog capture names in message group
def read_mess(file_one):
    data_file = json.load(open(file_one, 'r'))
    for p_name in data_file['participants']:
        add_name = p_name['name']
        if add_name not in sender_list:
            sender_list.append(add_name)
    return sender_list

def mess_count(data_files, sender_list):
    count = 0
    for name in sender_list:
        for parse_file in data_files:
            dt_file = json.load(open(parse_file, 'r'))
            for msg in dt_file['messages']:
                if msg['sender_name'] == name:
                    count += 1
        results[name] = count
    count = 0
    return results
     
# Cap names, then count messages per name
for z in data_files:
    read_mess(z)
mess_count(data_files, sender_list)

sort_res = sorted(results.items(), key=lambda x: x[1], reverse=True)
print(sort_res)
