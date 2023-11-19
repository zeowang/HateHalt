from sklearn.ensemble import AdaBoostClassifier, VotingClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import re
import pandas as pd
import pickle
import numpy as np


label_map = ['hate_speech', 'offensive_language', 'neither']

def combine_data():
    X1, y1 = load_data()
    X2, y2 = load_dgh()

    # Combine data using numpy.concatenate
    X = np.concatenate([X1, X2])
    y = np.concatenate([y1, y2])

    # Save X and y to CSV
    df = pd.DataFrame({'X': X, 'y': y})
    df.to_csv('backend/data/combined.csv', index=False)




def load_dgh():
    df = pd.read_csv('backend/data/dgh.csv')

    # Remove missing values
    df = df.dropna()



    X, y = df['text'].values, df['label'].values

    # if label is `hate` set to 1, if not then set of 0
    y = [1 if label == 'hate' else 0 for label in y]

    X = clean_strings(X)

    return X, y



def clean_strings(strings):
    regex = re.compile('[^a-z ]')  # Updated regex to include '#' and '@'
    for i in range(len(strings)):
        s = strings[i]
        s = s.lower()
        # remove all links
        s = re.sub(r"http\S+", "", s)
        # remove all mentions
        s = re.sub(r'@\S+', '', s)
        # remove all hashtags
        s = re.sub(r'#\S+', '', s)
        

        s = regex.sub('', s)
        s = re.sub(r'\s+', ' ', s).strip()
        # remove all leading and trailing space
        strings[i] = s

    return strings


def load_data():
    df = pd.read_csv('backend/data/labeled_data.csv')

    # Remove missing values
    df = df.dropna()

    # Remove duplicates
    df = df.drop_duplicates()

    # make sure the percentage of each class is the same
    df = df.groupby('class').head(3000)

    X, y = df['tweet'].values, df['class'].values
    
    X = clean_strings(X)

    # # if class is 0 or 1 set to 1, if class is 2 set to 0
    # y = [1 if label == 0 or label == 1 else 0 for label in y]

    return X, y


def fit(X, y):
    # Load the dataset
    laplace = 1
    texts = X
    labels = y
    X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.25, random_state=42)



    # Define n-gram ranges
    ngram_ranges = [(4, 5), (3, 4), (2, 3), (1, 2), (1, 1)]

    # Initialize individual classifiers
    classifiers = []
    for ngram_range in ngram_ranges:
        base_classifier = Pipeline([
            ('vectorizer', CountVectorizer(ngram_range=ngram_range)),
            ('classifier', MultinomialNB(alpha=laplace))
        ])

        classifiers.append(('clf_{}'.format(str(ngram_range)), base_classifier))

    # Create the ensemble model using VotingClassifier
    ensemble_classifier = VotingClassifier(classifiers, voting='soft')


    ensemble_classifier.fit(X_train, y_train)

    # Evaluate on the test set
    y_pred = ensemble_classifier.predict(X_test)

    # Evaluate the performance
    accuracy = accuracy_score(y_test, y_pred)
    print('Accuracy: {:.4f}'.format(accuracy))



    # save X_test and y_pred y_test to csv
    df = pd.DataFrame({'X_test': X_test, 'y_pred': y_pred, 'y_test': y_test})
    df.to_csv('backend/data/predictions.csv', index=False)

    # save the model to disk
    filename = 'backend/model/finalized_model.sav'
    pickle.dump(ensemble_classifier, open(filename, 'wb'))
    return ensemble_classifier


def load_model():
    # load the model from disk
    filename = 'backend/model/finalized_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    return loaded_model

def predict(strings, loaded_model):
    # clean strings remove all non-alphanumeric characters and replace with a ""
    strings = clean_strings(strings)
    labels = loaded_model.predict(strings)
    prob = loaded_model.predict_proba(strings)
    return labels, prob


if(__name__ == "__main__"):
    X, y = load_data()

    fit(X, y)

    strings = ["I wish you die", "I love eating", "I am sad", "very bad very bad very bad very bad very bad very bad very bad very bad very bad very bad"]

    model = load_model()
    result = predict(strings, model)
    print(result) 

    

    