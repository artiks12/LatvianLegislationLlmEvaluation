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
    instruction = f'Dots jautājums un vairākas atbildes. Cik juridiski pareizas ir sniegtās atbildes attiecībā uz Latvijas Republikas likumdošanu? Sniedz katrai atbildei vērtējumu no 0 līdz 100. Izdrukā tikai vērtējumus.\n'
    i = 0
    for type in data[d].keys():
        label = GetLabel(type, i)
        text = data[d][type].replace('\n',' ').replace('\r',' ')
        instruction += f'{label} {text}\n'
        i += 1
    instruction += '\n'
    lengths.append(len(instruction))
    if (len(instruction) < 24000):
        instructions.append(instruction)

instructions = sorted(instructions, key=len)

with open(f'ChatBotInstructions/chatbotEvaluation.txt', 'wt', encoding='utf-8') as f:
    f.writelines(instructions)

# print(sorted(lengths))
# print(len(lengths),len(instructions))