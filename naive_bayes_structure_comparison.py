"""
naive_bayes_structure_comparison.py

Holds functions to compare instances of NaiveBayesStructure
classes and their data structures
"""
from sklearn.naive_bayes import MultinomialNB
from numpy import array


def compare_structure(test, train):
    """
    Compares training and testing data for accuracy
    of the model
    """
    np_test = array(test)
    np_train = array(train)

    return _create_prediction_test(np_test, np_train)


def _create_prediction_test(np_test, np_train):
    """
    Makes the prediction for the test category
    """
    test_messages = np_test[:,0]
    test_category = np_test[:,1]

    train_messages = np_train[:,0]
    train_category = np_train[:,1]

    gnb = MultinomialNB()
    prediction = gnb.fit(list(train_messages), list(train_category)).predict(list(test_messages))

    return prediction, test_category


def predict_accuracy(d1, d2):
    """
    Determines the ratio of accurate predictions
    """
    correct = 0
    total = min(len(d1),len(d2))
    for i in range(total):
        if d1[i] == d2[i]:
            correct += 1

    return correct/total


def get_unpredicted(d1, d2):
    """
    Gets the indexs of unpredicted results
    """
    incorrect = []
    for i in range(min(len(d1),len(d2))):
        if d1[i] != d2[i]:
            incorrect.append(i)

    return incorrect
