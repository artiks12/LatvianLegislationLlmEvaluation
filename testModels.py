import os
from os import listdir
from os.path import isfile, join
import json
from pyquery import PyQuery as pq
import ollama

def WriteFile():
    pass

def ReadQuestionsFromFolder(path: str):
    if not os.path.exists(path):
        os.makedirs(path)
    # onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    onlyfiles = ['dati_2024_11.json']
    questions = []

    count = 0
    for file in onlyfiles:
        fullPath = path + '/' + file
        with open(fullPath, encoding='utf-8') as f:
            entries: list = json.load(f)
            count += len(entries)
            temp = [pq(entry['Saturi'][0]['Saturs']).text().replace('\n',' ') for entry in entries]
            questions.extend(temp)
    return questions


questions = ReadQuestionsFromFolder('lvportals')

# with open('test.txt', 'wt', encoding='utf-8') as f:
#     f.write('\n'.join(questions))

model = 'fl0id/teuken-7b-instruct-commercial-v0.4'

results = {
    'model': model,
    'Qs&As':[]
}
for question in questions:
    answer = ollama.generate(model=model, prompt=question)

    results['Qs&As'].append({
        'question': question,
        'answer': answer.response
    })

with open('modelTests/' + f'results_{model}.json', 'wt', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)