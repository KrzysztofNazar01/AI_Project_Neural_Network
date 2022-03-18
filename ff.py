from matplotlib import pyplot as plt
from sklearn.metrics import classification_report
from eli5.sklearn import PermutationImportance
from sklearn.model_selection import train_test_split
from keras.models import Sequential # for creating a linear stack of layers for our Neural Network 
from keras import Input # for instantiating a keras tensor 
from keras.layers import Dense # for creating regular densely-connected NN layer.
import math
import pandas as pd
import numpy as np
from keras.wrappers.scikit_learn import KerasClassifier
from variables import names, labels



def create_model(data):
    model = Sequential(name="A")
    model.add(Input(shape=(data.shape[1],), name="Input"))
    model.add(Dense(math.sqrt(data.shape[1]), activation='sigmoid', use_bias=True, name='Hidden-Layer'))
    model.add(Dense(math.sqrt(data.shape[1])/2, activation='sigmoid', use_bias=True, name='Hidden1'))
    model.add(Dense(math.sqrt(data.shape[1])/4, activation='sigmoid', use_bias=True, name='Hidden2'))
    # model.add(Dense(250, activation='softplus', use_bias=True, name='Hidden3'))
    model.add(Dense(1, activation='sigmoid', use_bias=True, name='Output'))
    model.compile(optimizer='adam', # default='rmsprop', an algorithm to be used in backpropagation
                  loss='binary_crossentropy', # Loss function to be optimized. A string (name of loss function), or a tf.keras.losses.Loss instance.
                  metrics=['accuracy', 'Precision', 'Recall'], # List of metrics to be evaluated by the model during training and testing. 
                 )
    return model


def keras(data):
    #model = KerasClassifier(build_fn=create_model,
    #          batch_size=2, # Number of samples per gradient update. If unspecified, batch_size will default to 32.
    #          epochs=200, # default=1, Number of epochs to train the model. An epoch is an iteration over the entire x and y data provided
    #          shuffle=True, # default=True, Boolean (whether to shuffle the training data before each epoch) or str (for 'batch').
    #          )

    model = create_model(data)
    X_train, X_test, y_train, y_test = train_test_split(np.asarray(data.toarray()), np.asarray(labels), shuffle=True)

    model.fit(X_train, y_train, batch_size=2, epochs=1000, verbose='auto', callbacks=None, shuffle=True, class_weight={0: 0.3, 1: 0.7}, sample_weight=None, initial_epoch=0, steps_per_epoch=None, validation_steps=None, validation_batch_size=None, validation_freq=3, max_queue_size=10, workers=1, use_multiprocessing=False)

    ##### Step 6 - Use model to make predictions
    # Predict class labels on training data
    pred_labels_tr = (model.predict(X_train) > 0.5).astype(int)
    # Predict class labels on a test data
    pred_labels_te = (model.predict(X_test) > 0.5).astype(int)

    #perm = PermutationImportance(model).fit(X_test, y_test)

    print('---------- Evaluation on Training Data ----------')
    print(classification_report(y_train, pred_labels_tr))
    print("")

    print('---------- Evaluation on Test Data ----------')
    print(classification_report(y_test, pred_labels_te))
    print("")

    #c = 0
    #importances = []
    #for i in perm.feature_importances_:
    #    importances.append([names[c], i])
    #    c += 1
    #print(sorted(importances, key = lambda x:x[1]))
    #fig, ax = plt.subplots()
    #y_size = np.arange(len(names))
    #ax.barh(y_size, perm.feature_importances_)
    #ax.set_yticks(y_size, labels = names)
    #ax.invert_yaxis()
    #ax.set_xlabel("Importance")
    #plt.show()


if __name__ == "__main__":
    keras()
