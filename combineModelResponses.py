import os
from os import listdir
from os.path import isfile, join
import json

def GetHypothesisAndReference(path: str, file):
    if not os.path.exists(path):
        os.makedirs(path)
    model = ''

    
    

    hyps = []
    refsROUGE = []
    refsBERT = []

    for d in data['Qs&As']:
        hyps.append(d['answer'])
        refsROUGE.append([d['gold']])
        refsBERT.append(d['gold'])
            
    return hyps, refsROUGE, refsBERT, model


path = 'modelResponses'

onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

result = {}

for file in onlyfiles:
    fullPath = path + '/' + file
    with open(fullPath, encoding='utf-8') as f:
        data = json.load(f)
    
    model = data['model'] + ';' + str(data['params']) + 'b'

    for d in range(len(data['Qs&As'])):
        if d not in result: result[d] = {}
        result[d]['question'] = data['Qs&As'][d]['question']
        result[d][model] = data['Qs&As'][d]['answer']

with open(f'combined_responses.json', 'wt', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
    