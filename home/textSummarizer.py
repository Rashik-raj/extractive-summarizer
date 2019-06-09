from .easyScrape import reqUrl
import re
import nltk
import heapq

def summarize(data):
    text = data

    #check if its url or text
    text_type = "text"    
    if data[0:5] == "https" or data[0:4] == "http":
        text_type = "URL"

    #this section is performed only if provided data is URL
    if text_type == "URL":
        page = reqUrl(data)
        text = ""
        for paragraph in page.find_all('p'):
            text += paragraph.text

    text = re.sub(r'\[[0-9]*\]',' ',text)            
    text = re.sub(r'\s+',' ',text)    
    clean_text = text.lower()
    clean_text = re.sub(r'\W',' ',clean_text)
    clean_text = re.sub(r'\d',' ',clean_text)
    clean_text = re.sub(r'\s+',' ',clean_text)
    sentences = nltk.sent_tokenize(text)
    stop_words = nltk.corpus.stopwords.words('english')

    word2count = {}  
    for word in nltk.word_tokenize(clean_text):     
        if word not in stop_words:                 
            if word not in word2count.keys():
                word2count[word]=1
            else:
                word2count[word]+=1

    for key in word2count.keys():                  
        word2count[key]=word2count[key]/max(word2count.values())

    sent2score = {}
    for sentence in sentences:
        for word in nltk.word_tokenize(sentence.lower()):
            if word in word2count.keys():
                if len(sentence.split(' '))<30:
                    if sentence not in sent2score.keys():
                        sent2score[sentence]=word2count[word]
                    else:
                        sent2score[sentence]+=word2count[word]


    best_sentences = heapq.nlargest(20,sent2score,key=sent2score.get)
    result = []
    for sentences in best_sentences:
        result.append(sentences)

    return result