import json
import pandas
from blacklist import blacklist, ignored_tokens
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from collections import Counter


def get_data():
    """Function that gets data from a file"""
    vv = TfidfVectorizer(stop_words='english')  # obiekt do liczenia slow
    with open("s.json", encoding="utf-8") as file:
        data = json.load(file)
    arr = []  # tabela z tekstami
    num_of_text = 60  # liczba analizowanych tekstów
    labels = []
    for i in range(0, num_of_text):
        labels.append(data[i]["isAntiVaccine"])
        st = data[i]["text"]
        st = st.lower()
        for j in ignored_tokens:
            st = st.replace(j, " ")
        st = ' '.join(filter(lambda x: blacklist.count(x) == 0, st.split(' ')))
        arr.append(st)
    vv.fit(arr)  # wrzuecnie do obiektu zeby zaczla liczyc
    print(vv.vocabulary_)  # drukowanie listy czestosci slow
    v = vv.transform(arr)  # zamiana na macierz
    print(v.toarray()[0])  # drukowanie pierwszego wiersza tej macierzy
    df = pandas.DataFrame(data=v.toarray(), columns=vv.get_feature_names())  # konwersja do koncowej tabelki
    print(df)  # drukowanie tabeli
    return v, labels


def classify(som, data, x_train, y_train):
    """Classifies each sample in data in one of the classes definited
    using the method labels_map.
    Returns a list of the same length of data where the i-th element
    is the class assigned to data[i].
    """
    winmap = som.labels_map(x_train, y_train)
    c = Counter(np.sum(list(winmap.values())))
    default_class = c.most_common()[0][0]
    result = []
    for d in data:
        win_position = som.winner(d)
        if win_position in winmap:
            result.append(winmap[win_position].most_common()[0][0])
        else:
            result.append(default_class)
    return result
