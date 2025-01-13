import os
from os import listdir
from os.path import isfile, join
import json
from pyquery import PyQuery as pq
import ollama
import re

def WriteFile():
    pass

def ReadQuestionsFromFolder(path: str):
    if not os.path.exists(path):
        os.makedirs(path)
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    questions = []
    gold = []

    count = 0
    for file in onlyfiles:
        fullPath = path + '/' + file
        with open(fullPath, encoding='utf-8') as f:
            entries: list = json.load(f)
            count += len(entries)
            temp = [re.sub(r'(\\n)+', ' ', pq(entry['Saturi'][0]['Saturs']).text()) for entry in entries]
            questions.extend(temp)
            temp = [re.sub(r'(\\n)+', ' ', pq(entry['Saturi'][1]['Saturs']).text())  for entry in entries]
            gold.extend(temp)
    return questions, gold


questions, gold = ReadQuestionsFromFolder('lvportals')

results = {
    'model': 'Human',
    'params': 0,
    'Qs&As':[]
}
for i in range(len(questions)):
    print(i)
    results['Qs&As'].append({
        'question': questions[i],
        'answer': gold[i]
    })

fullpath = 'modelResponses/' + f'results_0_human.json'
with open(fullpath, 'wt', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)
