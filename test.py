import json
import pandas
from blacklist import blacklist
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from minisom import MiniSom
vv = TfidfVectorizer(stop_words='english') #obiekt do liczenia slow
with open("s.json",encoding="utf-8") as file:
    data = json.load(file)
arr = [] #tabela z tekstami
numOfText = 25 #liczba analizowanych tekstów
labels = []
for i in range(0,60):
    labels.append(data[i]["isAntiVaccine"])
    st = data[i]["text"]
    st = st.lower()
    for j in blacklist:
        st = st.replace(j, " ")
    arr.append(st)
vv.fit(arr) #wrzuecnie do obiektu zeby zaczla liczyc
print(vv.vocabulary_) #drukowanie listy czestosci slow
v = vv.transform(arr) #zamiana na macierz

print(v.toarray()[0]) #drukowanie pierwszego wiersza tej macierzy
df = pandas.DataFrame(data=v.toarray(), columns=vv.get_feature_names()) #konwersja do koncowej tabelki
print(df)#drukowanie tabeli

def classify(som, data):
    """Classifies each sample in data in one of the classes definited
    using the method labels_map.
    Returns a list of the same length of data where the i-th element
    is the class assigned to data[i].
    """
    winmap = som.labels_map(X_train, y_train)
    default_class = np.sum(list(winmap.values())).most_common()[0][0]
    result = []
    for d in data:
        win_position = som.winner(d)
        if win_position in winmap:
            result.append(winmap[win_position].most_common()[0][0])
        else:
            result.append(default_class)
    return result

X_train, X_test, y_train, y_test = train_test_split(v.toarray(), labels, shuffle=False)

som = MiniSom(20, 20, 1491, sigma=10, learning_rate=0.5,
              neighborhood_function='triangle', random_seed=10)
som.pca_weights_init(X_train)
som.train_random(X_train, 500, verbose=False)

print(classification_report(y_test, classify(som, X_test)))

