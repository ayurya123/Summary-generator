import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest


# text="""“A restricted liquid’s external static pressure is “spread or transmitted uniformly throughout the liquid in all directions.”

# Any surface in contact with the fluid is at right angles to the static pressure’s action. Pascal discovered that for a static fluid, the pressure at a location would be the same for all planes going through the fluid. Pascal’s principle or the fluid-pressure transmission principle are other names for Pascal’s law. French mathematician 
# Blaise Pasca introduced the concept of Pascal law in 1653."""


def summarizer(rawdocs):
    stopwords= list(STOP_WORDS)
    # print(stopwords)
    nlp=spacy.load('en_core_web_sm')
    doc= nlp(rawdocs)
    # print(doc)
    tokens= [token.text for token in doc]
    # print(tokens)
    word_freq={}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text]=1
                
            else:
                word_freq[word.text]+=1
                
    # print(word_freq)  

    max_freq= max(word_freq.values())
    # print(max_freq)

    for word in word_freq.keys():
        word_freq[word]= word_freq[word]/max_freq
        
    # print(word_freq)    #normalised frequency

    sent_tokens=[sent for sent in doc.sents]
    # print(sent_tokens)

    sent_scores={}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent]=word_freq[word.text]
                else:
                    sent_scores[sent]+=word_freq[word.text]    
                    
    # print(sent_scores)  

    select_len= int(len(sent_tokens)*0.5) #50% of total length of sentence

    # nlargest basically print the sentence with high freq
    summary= nlargest(select_len, sent_scores,key=sent_scores.get)  
    # print(summary)  

    final_summary= [word.text for word in summary] 
    summary= ' '.join(final_summary)
    # print(text)
    # print(summary)    
    # print("Length of original text ",len(text.split(' ')))
    # print("Length of summary text ",len(summary.split(' ')))
    return summary,doc, len(rawdocs.split(' ')), len(summary.split(' '))
