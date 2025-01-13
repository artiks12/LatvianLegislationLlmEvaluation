from pyquery import PyQuery as pq
import json

HTML_FOLDER = 'WebChatHtmlFiles/'
QUESTION_FOLDER = 'modelResponses/References/'

def GetSpecificQuestions(ids, HtmlFile, ModelFile, startElement, answerElement, questionElement = '', last = False):
    with open(HTML_FOLDER + HtmlFile, 'r', encoding='utf-8') as f:
        html_content = pq(f.read())

    answer_sets = html_content(startElement)

    all_pairs = {}

    even = False
    question = ''
    for answer_set in answer_sets.items():
        for answer in answer_set.items():
            if questionElement == '':
                if not(even): 
                    question = answer(answerElement).text()
                    if question not in all_pairs.keys(): all_pairs[question] = ''
                else:
                    if all_pairs[question] == '' or last:
                        all_pairs[question] = answer(answerElement).text()
            else:
                question = answer(questionElement).text()
                if question not in all_pairs.keys(): all_pairs[question] = ''
                if all_pairs[question] == '' or last:
                    all_pairs[question] = answer(answerElement).text()
            even = not(even)

    fullPath = QUESTION_FOLDER + ModelFile

    with open(fullPath, encoding='utf-8') as f:
        content = json.load(f)

    print(len(all_pairs))
    count = 0
    for i in all_pairs.keys():
        content['Qs&As'][ids[count]]['answer'] = all_pairs[i]
        count += 1

    with open(fullPath, 'wt', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=4)


def fetchData(HtmlFile, ModelFile, startElement, answerElement, questionElement = '', last = False):
    with open(HTML_FOLDER + HtmlFile, 'r', encoding='utf-8') as f:
        html_content = pq(f.read())

    answer_sets = html_content(startElement)

    all_pairs = {}

    even = False
    question = ''
    for answer_set in answer_sets.items():
        for answer in answer_set.items():
            if questionElement == '':
                if not(even): 
                    question = answer(answerElement).text()
                    if question not in all_pairs.keys(): all_pairs[question] = ''
                else:
                    if all_pairs[question] == '' or last:
                        all_pairs[question] = answer(answerElement).text()
            else:
                question = answer(questionElement).text()
                if question not in all_pairs.keys(): all_pairs[question] = ''
                if all_pairs[question] == '' or last:
                    all_pairs[question] = answer(answerElement).text()
            even = not(even)

    fullPath = QUESTION_FOLDER + ModelFile

    with open(fullPath, encoding='utf-8') as f:
        content = json.load(f)

    print(len(all_pairs))
    count = 0
    for i in all_pairs.keys():
        content['Qs&As'][count]['answer'] = all_pairs[i]
        count += 1

    with open(fullPath, 'wt', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=4)


fetchData('ChatGPT.html', 'results_chatGPT-4o-mini.json', 'article', 'div.flex.max-w-full.flex-col.flex-grow')
fetchData('Gemini2.html', 'results_gemini-2.0-flash.json', 'div.conversation-container.message-actions-hover-boundary.response-optimization.eighty-char-code-block.tts-removed.ng-star-inserted', 'message-content', 'div.query-content', True)
fetchData('Gemini1.5.html', 'results_gemini-1.5-flash.json', 'div.conversation-container.message-actions-hover-boundary.response-optimization.eighty-char-code-block.tts-removed.ng-star-inserted', 'message-content', 'div.query-content', True)

GetSpecificQuestions([253],'Gemini2.0_Q254.html', 'results_gemini-2.0-flash.json', 'div.conversation-container.message-actions-hover-boundary.response-optimization.eighty-char-code-block.tts-removed.ng-star-inserted', 'message-content', 'div.query-content', True)
GetSpecificQuestions([253],'Gemini1.5_Q254.html', 'results_gemini-1.5-flash.json', 'div.conversation-container.message-actions-hover-boundary.response-optimization.eighty-char-code-block.tts-removed.ng-star-inserted', 'message-content', 'div.query-content', True)
