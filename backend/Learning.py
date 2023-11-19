from sklearn.ensemble import VotingClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import re
import pandas as pd
import pickle



# class NaiveBayes:

#     def __init__(self, beta, num_classes):
#         self.beta= beta 
#         self.clf = MultinomialNB(alpha=beta)
#         self.vectorizer = CountVectorizer()
#         self.num_classes = num_classes


    
    
#     def fit(self, X, y):
#         # fit the model
#         self.clf.fit(X, y)
#         return self.clf

        


#     def predict(self, X, y):
#         self.clf.predict(X)
    



    

# class NaiveBayesNgrams(NaiveBayes):
#     def __init__(self, num_classes, ngram_range=(1, 1), beta=0):
#         super().__init__(num_classes, beta)
#         self.vectorizer = CountVectorizer(ngram_range=ngram_range)
#         self.clf = MultinomialNB(alpha=beta)
    
#     def fit(self, X, y):
#         X, y = self.preprocess(X, y)
        
#         super().fit(X, y)
#         return self.clf


#     def predict(self, X, y):
#         X, y = self.preprocess(X, y)
#         y_pred = self.clf.predict(X)
#         return y_pred

#     def preprocess(self, X, y):
#         # input X is a list of strings

#         # clean strings remove all non-alphanumeric characters and replace with a ""
#         X = X.str.replace('[^a-zA-Z0-9]', ' ')

#         # Convert the text to lowercase
#         X = X.str.lower()

#         # make the data to be n-grams
#         X = self.vectorizer.fit_transform(X)
#         return X, y


def load_data():
    df = pd.read_csv('backend/data/labeled_data.csv')
    df = df[['tweet', 'class']]

    # Remove missing values
    df = df.dropna()

    # Remove duplicates
    df = df.drop_duplicates()

    # make sure the percentage of each class is the same
    df = df.groupby('class').head(2000)

    X, y = df['tweet'].values, df['class'].values

    regex = re.compile('[^a-z ]')  # Updated regex to include '#' and '@'

    # 
    for i in range(len(X)):
        X[i] = X[i].lower()
        # remove all links
        X[i] = re.sub(r"http\S+", "", X[i])
        # remove all mentions
        X[i] = re.sub(r'@\S+', '', X[i])
        # remove all hashtags
        X[i] = re.sub(r'#\S+', '', X[i])
        

        X[i] = regex.sub('', X[i])
        X[i] = re.sub(r'\s+', ' ', X[i]).strip()
        # remove all leading and trailing space

    return X, y





def fit(X, y):
    # Load the dataset

    texts = X
    labels = y
    X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.25, random_state=42)

    # Define n-gram ranges
    ngram_ranges = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]

    # Initialize individual classifiers
    classifiers = []
    for ngram_range in ngram_ranges:
        clf = Pipeline([
            ('vectorizer', CountVectorizer(ngram_range=ngram_range)),
            ('classifier', MultinomialNB())
        ])
        classifiers.append(('clf_{}'.format(str(ngram_range)), clf))

    # Create the ensemble model using VotingClassifier
    ensemble_classifier = VotingClassifier(classifiers, voting='soft')

    # Train the ensemble model
    ensemble_classifier.fit(X_train, y_train)

    # Initialize voting classifier
    ensemble_classifier = VotingClassifier(classifiers, voting='soft')

    # Train the voting classifier
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
    filename = 'finalized_model.sav'
    pickle.dump(ensemble_classifier, open(filename, 'wb'))


def load_model():
    # load the model from disk
    filename = 'finalized_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    return loaded_model

def predict(strings):
    # load the model from disk
    filename = 'finalized_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    result = loaded_model.predict(strings)
    return result


if(__name__ == "__main__"):
    X, y = load_data()
    fit(X, y)

    strings = ["I love you", "I hate you", "I am sad", "I am happy"]

    result = predict(strings)
    print(result)   


    

    