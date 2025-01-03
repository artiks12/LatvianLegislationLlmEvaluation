from rouge_metric import PyRouge
from bert_score import BERTScorer, score
import os
from os import listdir
from os.path import isfile, join
import json

def GetHypothesisAndReference(path: str, file):
    if not os.path.exists(path):
        os.makedirs(path)
    model = ''

    fullPath = path + '/' + file
    with open(fullPath, encoding='utf-8') as f:
        data = json.load(f)
    
    model = data['model'] + ';' + str(data['params']) + 'b'

    hyps = []
    refsROUGE = []
    refsBERT = []

    for d in data['Qs&As']:
        hyps.append(d['answer'])
        refsROUGE.append([d['gold']])
        refsBERT.append(d['gold'])
            
    return hyps, refsROUGE, refsBERT, model

def FixRougeScores(ROUGEscores: dict):
    for metric in ROUGEscores.keys():
        ROUGEscores[metric]['r'] = round(ROUGEscores[metric]['r'], 4)
        ROUGEscores[metric]['p'] = round(ROUGEscores[metric]['p'], 4)
        ROUGEscores[metric]['f'] = round(ROUGEscores[metric]['f'], 4)

def GetROUGEforSeparateSentences(hyps, refs):
    if len(hyps) == len(refs):
        for i in range(len(hyps)):
            hyp = [hyps[i]]
            ref = [refs[i]]
            scores = rouge.evaluate(hyp, ref)
            finalScores = {
                'ROUGE-1': scores['rouge-1']['r'],
                'ROUGE-2': scores['rouge-2']['f'],
                'ROUGE-4': scores['rouge-4']['f'],
                'ROUGE-L': scores['rouge-l']['f'],
                'ROUGE-W': scores['rouge-w-1.2']['f'],
                'ROUGE-S': scores['rouge-s4']['f'],
                'ROUGE-SU': scores['rouge-su4']['f'],
            }
            if finalScores['ROUGE-L'] > 0.2:
                print(i, finalScores)


path = 'modelResponses'

onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
# onlyfiles = ['results_llama3.2.json']
rouge = PyRouge(rouge_n=(1, 2, 4), rouge_l=True, rouge_w=True,
    rouge_w_weight=1.2, rouge_s=True, rouge_su=True, skip_gap=4)
bert = BERTScorer(lang='lv')

for file in onlyfiles:
    hyps, refsROUGE, refsBERT, model = GetHypothesisAndReference(path, file)
    print(model)
    ROUGEscores = rouge.evaluate(hyps, refsROUGE)
    FixRougeScores(ROUGEscores)
    P_bert, R_bert, F1_bert = score(hyps, refsBERT, lang='lv',verbose=True)
    result = {
        'model': model,
        'ROUGE': ROUGEscores,
        'BERTScore': {
            'p': round(P_bert.mean().item(),4),
            'r': round(R_bert.mean().item(),4),
            'f': round(F1_bert.mean().item(),4)
        }
    }
    model = model.replace(':','_').replace('/',';')
    with open(f'scores/scores_{model}.json', 'wt', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    # GetROUGEforSeparateSentences(hyps, refsROUGE)
    