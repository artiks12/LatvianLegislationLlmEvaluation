import os
from os import listdir
from os.path import isfile, join
import json

def GetInstructions(path: str, file):
    if not os.path.exists(path):
        os.makedirs(path)
    model = ''

    fullPath = path + '/' + file
    with open(fullPath, encoding='utf-8') as f:
        data = json.load(f)
    
    model = data['model'] + ';' + str(data['params']) + 'b'

    instructions = []

    for d in data['Qs&As']:
        instruction = f'''Dots jautājums un divas atbildes. Cik juridiski pareizas ir sniegtās atbildes attiecībā uz Latvijas Republikas likumdošanu? Sniedz katrai atbildei vērtējumu no 0 līdz 100 un neko vairāk.
Jautājums: {d['question']}
1. atbilde: {d['gold']}
2. atbilde: {d['answer']}
\n'''
        instructions.append(instruction)
    
    return model, instructions

path = 'modelTests'

onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
for file in onlyfiles:
    model, instructions = GetInstructions(path, file)
    with open(f'chatGptInstructions/instructions_{model}.txt', 'wt', encoding='utf-8') as f:
        f.writelines(instructions)