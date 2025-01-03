import statistics
import json
import math

def getStats(model, data):
    quantiles = statistics.quantiles(data,n=100)
    return {
        'name': model,
        'min': min(data),
        'max': max(data),
        'avg': statistics.mean(data),
        'median': statistics.median(data),
        'p98': math.ceil(quantiles[-2]),
        'p99': math.ceil(quantiles[-1])
    }

data = {}

combined = ['' for _ in range(277)]

with open('combined_responses.json', encoding='utf-8') as f:
    texts = json.load(f)

    models = list(texts['0'].keys())[1:]

    for model in models:
        data[model] = []
        for t in texts:
            data[model].append(len(texts[t][model]))
            combined[int(t)] += texts[t][model]

data['combined'] = [len(text) for text in combined]

for model in data:
    print(getStats(model, data[model]))