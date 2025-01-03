import os
from os import listdir
from os.path import isfile, join
import json

lengths = []

def GetLabel(key,i):
    if key == 'question': return 'Jautājums:'
    return f'{i}. Atbilde:'

instructions = []

with open('combined_responses.json', encoding='utf-8') as f:
    data = json.load(f)

for d in data:
    text = data[d]["question"].replace('\n',' ').replace('\r',' ')
    instruction = f'''Dots jautājums. Atbildi juridiski pareizi uz šo jautājumu Latvijas Republikas kontekstā. Lūdzu sniedz tikai atbildi.:
Jautājums: {text}\n'''
    instruction += '\n'
    instructions.append(instruction)

with open(f'chatGptQuestions.txt', 'wt', encoding='utf-8') as f:
    f.writelines(instructions)