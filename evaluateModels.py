from rouge_metric import PyRouge
from bert_score import BERTScorer, score
from Metrics.UniEval.utils import convert_to_json
from Metrics.UniEval.metric.evaluator import get_evaluator
from Metrics.BARTScore.bart_score import BARTScorer
from moverscore_v2 import get_idf_dict, word_mover_score
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
    rouge = PyRouge(rouge_n=(1, 2, 4), rouge_l=True, rouge_w=True,
        rouge_w_weight=1.2, rouge_s=True, rouge_su=True, skip_gap=4)
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
    del rouge

def GetTrueRougeScores(scores):
    return {
        'ROUGE-1': round(scores['rouge-1']['r'], 4),
        'ROUGE-2': round(scores['rouge-2']['f'], 4),
        'ROUGE-4': round(scores['rouge-4']['f'], 4),
        'ROUGE-L': round(scores['rouge-l']['f'], 4),
        'ROUGE-W': round(scores['rouge-w-1.2']['f'], 4),
        'ROUGE-S': round(scores['rouge-s4']['f'], 4),
        'ROUGE-SU': round(scores['rouge-su4']['f'], 4)
    }

def GetRougeScores(hyps, refs):
    rouge = PyRouge(rouge_n=(1, 2, 4), rouge_l=True, rouge_w=True,
        rouge_w_weight=1.2, rouge_s=True, rouge_su=True, skip_gap=4)
    
    ROUGEscores = rouge.evaluate(hyps, refs)
    del rouge
    return GetTrueRougeScores(ROUGEscores)

def GetBartScore(hyps, refs):
    bart = BARTScorer(device='cuda:0', checkpoint='facebook/bart-large-cnn')

    BARTscores = bart.multi_ref_score(hyps, refs, batch_size=4)
    del bart
    return round(sum(BARTscores)/len(BARTscores),4)

def GetBertScore(hyps, refs):
    bert = BERTScorer(lang='lv')
    
    P_bert, R_bert, F1_bert = bert.score(hyps, refs, verbose=False)
    del bert
    return round(F1_bert.mean().item(),4)

def GetUniEvalScores(hyps, refs):
    unieval = get_evaluator('fact')
    UniEvalData = convert_to_json(output_list=hyps, src_list=refs)

    UniEvalScores = unieval.evaluate(UniEvalData)
    del unieval
    return round(sum( [score['consistency'] for score in UniEvalScores])/len(UniEvalScores),4)

def GetMoverScore(hyps, refs):
    idf_dict_hyp = get_idf_dict(refs) # idf_dict_hyp = defaultdict(lambda: 1.)
    idf_dict_ref = get_idf_dict(hyps) # idf_dict_ref = defaultdict(lambda: 1.)

    MoverScores = word_mover_score(refs, hyps, idf_dict_hyp, idf_dict_ref, batch_size=128)
    return round(sum(MoverScores)/len(MoverScores),4)

if __name__ == '__main__':
    path = 'ModelResponses/References'

    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

    for file in onlyfiles:
        # refsROUGE - liist of lists, refsBERT - list of strings
        hyps, refsROUGE, refsBERT, model = GetHypothesisAndReference(path, file)
        print(model)
        
        print('Calculating ROUGE')
        ROUGEscores = GetRougeScores(hyps, refsROUGE)
        print('Calculating BARTScore')
        BARTscore = GetBartScore(hyps, refsROUGE)
        print('Calculating BERTScore')
        BERTscore = GetBertScore(hyps, refsBERT)
        print('Calculating MoverScore')
        MoverScore = GetMoverScore(hyps, refsBERT)
        # print('Calculating UniEval')
        # UniEvalScores = GetUniEvalScores(hyps, refsBERT)
        result = {
            'model': model,
            'ROUGE': ROUGEscores,
            'BERTScore': BERTscore,
            'BARTScore': BARTscore,
            # 'UniEval': UniEvalScores,
            'MoverScore': MoverScore
        }
        model = model.replace(':','_').replace('/',';')
        with open(f'scores/scores_{model}.json', 'wt', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        # GetROUGEforSeparateSentences(hyps, refsROUGE)
    