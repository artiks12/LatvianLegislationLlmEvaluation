from pyquery import PyQuery as pq
import json

HTML_FOLDER = 'WebChatHtmlFiles/'
QUESTION_FOLDER = 'modelResponses/References/'
    
def fetchData(HtmlFile, ModelFile, startElement, answerElement, needEvenCheck = False):
    with open(HTML_FOLDER + HtmlFile, 'r', encoding='utf-8') as f:
        html_content = pq(f.read())

    answer_sets = html_content(startElement)

    all_answers = []
    all_questions = []

    if needEvenCheck: even = False
    skip = False

    for answer_set in answer_sets.items():
        count = 0
        for answer in answer_set.items():
            if answer(answerElement).text() in all_questions:
                if needEvenCheck: even = True
                skip = True
                continue
            all_questions.append(answer(answerElement).text())
            if needEvenCheck:
                if not(even):
                    even = True
                    continue
            if skip:
                if needEvenCheck: even = False
                skip = False
                continue
            
            count += 1
            text = answer(answerElement).text()
            # text = text.replace('\n',' ').replace('\r',' ').replace(' ',' ')
            all_answers.append(text)
            even = False

    fullPath = QUESTION_FOLDER + ModelFile

    with open(fullPath, encoding='utf-8') as f:
        content = json.load(f)

    print(len(all_answers))
    for i in range(len(all_answers)):
        if content['Qs&As'][i]['answer'] == "":
            content['Qs&As'][i]['answer'] = text

    with open(fullPath, 'wt', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=4)


# fetchData('ChatGPT.html', 'results_chatGPT-4o-mini.json', 'article', 'div.flex.max-w-full.flex-col.flex-grow', True)
fetchData('Gemini2.html', 'results_gemini-2.0-flash.json', 'div.conversation-container.message-actions-hover-boundary.response-optimization.eighty-char-code-block.tts-removed.ng-star-inserted', 'message-content')
# fetchData('Gemini1.5.html', 'results_gemini-1.5-flash.json', 'div.conversation-container.message-actions-hover-boundary.response-optimization.eighty-char-code-block.tts-removed.ng-star-inserted', 'message-content')

