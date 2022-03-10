from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from minisom import MiniSom
from functions import classify, get_data

data, labels = get_data()

X_train, X_test, y_train, y_test = train_test_split(data.toarray(), labels, shuffle=False)
som = MiniSom(20, 20, data.shape[1], sigma=18, learning_rate=0.1,
              neighborhood_function='triangle', random_seed=10)
som.pca_weights_init(X_train)
som.train_random(X_train, 500, verbose=False)

print(classification_report(y_test, classify(som, X_test, X_train, y_train)))

#wizualiacja - rysowanie siatki SOM
#zobaczyc na TF a znie na cale TFIDF

#dredukowac z1500 do 200
#wyrac najsitotniejsze slowa
#part of speedch taging
#pokolorac wszgledem  0 i 1
#wpraowdzic nowa siec FitFowrawd  - wezmie polowe tych tekstow i sie przetrenuje (bedzie trnowana na tej zredukowanej tabeli)
#dolozyc tesktow
#ktore slowa sa klczowe do wskania ze dany tekst nalezy do konkretnej klasy







