import json
import os
import datetime

def year_month_range(start_year, end_year):
    for year in range(start_year, end_year + 1):
        for month in range(1,13):
            yield '{}-{}'.format(year, str(month).zfill(2))
            
def colors():
    color_list = ['#79d70f',
                  '#d32626', 
                  '#f5a31a', 
                  '#5fdde5', 
                  '#f4ea8e', 
                  '#6a097d', 
                  '#fa744f', 
                  '#16817a', 
                  '#ffd8a6', 
                  '#ff427f', 
                  '#c1a57b', 
                  '#aacfcf']
    for c in color_list:
        yield c
        
def timestamp_to_month(epoch_ms):
    return datetime.datetime.fromtimestamp(epoch_ms/1000.0).strftime('%Y-%m')
    
def get_all_messages(data_files):
    messages = []
    for data_file in data_files:
        messages += data_file['messages']
    messages.sort(key=lambda x: x['timestamp_ms'])
    return messages

def get_participants(messages):
    return set(m['sender_name'] for m in messages)
    
class MessageStats:
    LAUGHTER_WORDS = ['Hahah','lol','haha','hahaha','lmao','lolz','lols']
        
    def __init__(self, message=None):
        if not message:
            return
        self.count = 1
        self.total_words = len(message['content'].split())
        self.total_laughs = sum(message['content'].lower().count(kw) for kw in MessageStats.LAUGHTER_WORDS)
        self.sender_name = message['sender_name']
        
    def __add__(self, other_message_stats):
        sum_stats = MessageStats()
        sum_stats.count = self.count + other_message_stats.count
        sum_stats.total_words = self.total_words + other_message_stats.total_words
        sum_stats.total_laughs = self.total_laughs + other_message_stats.total_laughs
        return sum_stats
    
    def __repr__(self):
        return str({'Message Count': self.count,
                    'Total Words': self.total_words,
                    'Total Laughs': self.total_laughs})
    
    def __str__(self):
        return repr(self)

def get_bucketed_message_stats(messages, bucket_key_function):
    stats_by_bucket = {}
    for message in messages:
        try:
            stats = MessageStats(message)
            bucket_key = bucket_key_function(message)
            if bucket_key in stats_by_bucket:
                stats_by_bucket[bucket_key] = stats_by_bucket[bucket_key] + stats
            else:
                stats_by_bucket[bucket_key] = stats
        except:
            pass
    return stats_by_bucket

def get_message_stats_by_name(messages):
    return get_bucketed_message_stats(messages, lambda stats: stats['sender_name'])

def get_message_stats_timeseries(messages):
    bucketed_stats = get_bucketed_message_stats(messages, lambda stats: (stats['sender_name'] + timestamp_to_month(stats['timestamp_ms'])))
    year_months = list(year_month_range(2012, 2020))
    participants = get_participants(messages)
    datasets = []
    color_gen = colors()
    for p in participants:
        data = []
        for ym in year_months:
            bucket_key = p + ym
            if bucket_key in bucketed_stats:    
                data.append(bucketed_stats[bucket_key].count)
            else:
                data.append(0)
        datasets.append({'label': p, 'data': data, 'backgroundColor': next(color_gen)})
    return {
        'data': {
            'labels': year_months, 
            'datasets': datasets}
        }


# Get files in folder first for batch processing in .py folder.     
data_filenames = [data_file for data_file in os.listdir() 
              if data_file.endswith('.json')]
data_files = [json.load(open(f, 'r')) for f in data_filenames]

messages = get_all_messages(data_files)
print(get_message_stats_by_name(messages))

with open('time_series.js','w') as f: 
     f.write(json.dumps(get_message_stats_timeseries(messages)))
