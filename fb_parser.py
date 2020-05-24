import json
import os

# Dump lists
sender_list = []
data_files = []
results = {}

# Get files in folder first for batch processing.
file_list = os.listdir()
for y in file_list:
    if y[-5:] == '.json':
        data_files.append(y)

# Prog capture names in message group.
def read_mess(data_files):
    for dt_file in data_files:
        data_file = json.load(open(dt_file, 'r'))
        for p_name in data_file['participants']:
            add_name = p_name['name']
            if add_name not in sender_list:
                sender_list.append(add_name)
    return sender_list

# 'mess_count' to capture total messages sent over time.
def message_data(data_files, sender_list):
    mess_count = 0
    tot_words = 0
    for name in sender_list:
        for parse_file in data_files:
            dt_file = json.load(open(parse_file, 'r'))
            for msg in dt_file['messages']:
                if msg['sender_name'] == name:
                    mess_count += 1
                    #tot_words += len(msg['content'].split())
        results[name] = mess_count, (tot_words / mess_count)
    mess_count = 0
    tot_words = 0
    return results

# Processing
read_mess(data_files)
message_data(data_files, sender_list)

# Outputs
sort_res = sorted(results.items(), key=lambda x: x[1], reverse=True)
print(sort_res)
