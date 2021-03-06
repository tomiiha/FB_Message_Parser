import json
import os

# Data dump
sender_list = []
data_files = []
results = {}

# Get files in folder first for batch processing in .py folder.
file_list = os.listdir()
for y in file_list:
    if y[-5:] == '.json':
        data_files.append(y)

# Prog capture names in message group - then pass this for parsing.
def participants(data_files):
    for parse_file in data_files:
        dt_file = json.load(open(parse_file, 'r'))
        for p_name in dt_file['participants']:
            add_name = p_name['name']
            if add_name not in sender_list:
                sender_list.append(add_name)
    return base_mess_data(data_files, sender_list)

# 'mess_count' to capture total messages sent over time.
# 'tot_words' number of messages sent.
# 'tot_laugh' calculates the total of open laughter in messages.
def base_mess_data(data_files, sender_list):
    mess_count = 0
    tot_words = 0
    tot_laugh = 0
    for name in sender_list:
        for parse_file in data_files:
            dt_file = json.load(open(parse_file, 'r'))
            for msg in dt_file['messages']:
                if msg['sender_name'] == name:
                    mess_count += 1
                    try:
                        tot_words += len(msg['content'].split())
                        tot_laugh += msg['content'].count('Haha')
                        tot_laugh += msg['content'].count('lol')
                    except:
                        pass
        results[name] = [mess_count, round((tot_words / mess_count),2), tot_laugh]
        mess_count = 0
        tot_words = 0
        tot_laugh = 0
    return results

# Processing
participants(data_files)
print(results)
