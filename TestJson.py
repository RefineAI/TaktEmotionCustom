import json


frame = {}
frame["userId"] = "test"
frame["videoId"] = "testVideo"
frame['report'] = []

results = {}
results['customer'] = {}
emotion = {}
emotions ={}
head = {}

frame['report'].append['customer'] = {'name':'pandu', 'place':'gandu'}

frame['report'].append['emotions'] = {'some':'value'}
frame['report'].append['emotion'] = {'ano':'val'}
frame['report'][0]['head'] = {'head':'phir'}
frame['report'][0]['eyes'] = {'left':'x','right':'y'}
frame['report'][0]['result'] = {'overall': 'zero'}

frame['report'][1]['customer'] = {'another':'cust', 'good':'bad'}

str = json.dumps(frame)

obj = json.loads(str)

print frame
print obj['report'][0]['customer']['place']


