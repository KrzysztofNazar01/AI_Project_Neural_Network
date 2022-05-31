from som import som, plotSom
# from ff import keras
# from svm import getImportantData
from func import get_word_embeddings2, get_word_embeddings
import numpy as np

"""
    SOM map is generated. Data to model is provided by the getImportantData() function. 
"""


def saveDistanceInfoToExcelFile(distances):
    import xlsxwriter
    workbook = xlsxwriter.Workbook('SOMNeuronDistances.xlsx')
    worksheet = workbook.add_worksheet()

    # write column names
    columnNames = ["LearningRate", "sumFor", "avgFor", "sumAgainst", "avgAgainst"]
    for iter in range(len(columnNames)):
        worksheet.write(0, iter, columnNames[iter])

    # calcualte differences between before and after values
    additionalSize = int(len(distances) / 2)
    allSize = len(distances) + additionalSize
    distances.append([0, 0, 0, 0, 0])
    for rowIter in range(2, allSize, 3):
        newRow = []
        size = len(distances[rowIter])
        for colIter in range(len(distances[rowIter]) - 1, 0, -1):
            valueBefore = distances[rowIter - 2][colIter]
            valueAfter = distances[rowIter - 1][colIter]
            newRow.insert(0, round(valueAfter - valueBefore, 2))
        newRow.insert(0, distances[rowIter - 2][0])  # Learning rate value

        distances.insert(rowIter, newRow)

    # save the distance Data into file
    row = 1
    cols = 5
    for data in distances[:-1]:  # last row is filled with zeros
        for i in range(cols):
            worksheet.write(row, i, data[i])
        row += 1

    workbook.close()


if __name__ == "__main__":
    _, data, labels, names = get_word_embeddings(.0, .8)
    _, data2, labels, names = get_word_embeddings(.8, 1.0)
    _, data3, labels, names = get_word_embeddings()

    distances = []

    sommodel = som(data, .15)
    distances.append(plotSom(sommodel, data, labels, names, 0.15))
    sommodel.train_random(data2, 50)
    distances.append(plotSom(sommodel, data3, labels, names, 0.15))

    sommodel = som(data, .1)
    distances.append(plotSom(sommodel, data, labels, names, 0.1))
    sommodel.train_random(data2, 50)
    distances.append(plotSom(sommodel, data3, labels, names, 0.1))

    sommodel = som(data, .01)
    distances.append(plotSom(sommodel, data, labels, names, 0.01))
    sommodel.train_random(data2, 50)
    distances.append(plotSom(sommodel, data3, labels, names, 0.01))

    sommodel = som(data, .001)
    distances.append(plotSom(sommodel, data, labels, names, 0.001))
    sommodel.train_random(data2, 50)
    distances.append(plotSom(sommodel, data3, labels, names, 0.001))

    sommodel = som(data, .0001)
    distances.append(plotSom(sommodel, data, labels, names, 0.0001))
    sommodel.train_random(data2, 50)
    distances.append(plotSom(sommodel, data3, labels, names, 0.0001))

    saveDistanceInfoToExcelFile(distances)
