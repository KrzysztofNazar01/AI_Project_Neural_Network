import json
import nltk
import pandas
from blacklist import blacklist, ignored_tokens, tag_list
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from collections import Counter

with open("s.json", encoding="utf-8") as file:
    data = json.load(file)
num_of_text = len(data)  # liczba analizowanych tekstów


def get_data():
    """Function that gets data from a file"""
    vectorizer = TfidfVectorizer(stop_words='english', min_df=0.035)  # obiekt do liczenia slow
    arr = []  # tabela z tekstami
    labels = []
    for i in range(0, num_of_text):
        labels.append(data[i]["isAntiVaccine"])
        st = data[i]["text"]
        st = st.lower()
        for j in ignored_tokens:
            st = st.replace(j, " ")
        tokens = nltk.word_tokenize(st)
        tags = nltk.pos_tag(tokens)
        for (word, tag) in tags:
            if tag in tag_list:
                tokens.remove(word)
        st = ' '.join(filter(lambda x: blacklist.count(x) == 0, tokens))
        arr.append(st)
    vectorizer.fit(arr)  # wrzuecnie do obiektu zeby zaczla liczyc
    v = vectorizer.transform(arr)  # zamiana na macierz
    print(vectorizer.vocabulary_)
    return v, labels, vectorizer.get_feature_names()


def get_important(vocab):
    """Function that transforms vocab into vector space"""
    vectorizer = TfidfVectorizer()  # obiekt do liczenia slow
    arr = []  # tabela z tekstami
    for i in range(0, num_of_text):
        temp = []
        st = data[i]["text"]
        st = st.lower()
        tokens = st.split()
        for word in tokens:
            if word in vocab:
                temp.append(word)
        st = ' '.join(temp)
        arr.append(st)
    vectorizer.fit(arr)  # wrzuecnie do obiektu zeby zaczla liczyc
    v = vectorizer.transform(arr)  # zamiana na macierz
    print(vectorizer.vocabulary_)
    print(len(vocab))
    print(len(vectorizer.vocabulary_))
    df = pandas.DataFrame(data=v.toarray(), columns=vectorizer.get_feature_names())
    print(df)
    return v, vectorizer.get_feature_names()
