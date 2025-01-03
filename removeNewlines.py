text = ''''''

import json

fullPath = 'modelResponses/References/' + 'results_chatGPT-4o-mini.json'
with open(fullPath, encoding='utf-8') as f:
    content = json.load(f)

text = text.replace('\n',' ').replace('\r',' ').replace(' ',' ')

for i in range(len(content['Qs&As'])):
    if content['Qs&As'][i]['answer'] == "":
        content['Qs&As'][i]['answer'] = text
        break

with open(fullPath, 'wt', encoding='utf-8') as f:
    json.dump(content, f, ensure_ascii=False, indent=4)
