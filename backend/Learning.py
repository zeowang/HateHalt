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
    df = df[['tweet', 'class']]

    # Remove missing values
    df = df.dropna()

    # Remove duplicates
    df = df.drop_duplicates()

    # make sure the percentage of each class is the same
    df = df.groupby('class').head(2000)

    X, y = df['tweet'].values, df['class'].values
    
    X = clean_strings(X)
        

    return X, y





def fit(X, y):
    # Load the dataset
    laplace = 0.1
    texts = X
    labels = y
    X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.25, random_state=42)



    # Define n-gram ranges
    ngram_ranges = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]

    # Initialize individual classifiers
    classifiers = []
    for ngram_range in ngram_ranges:
        clf = Pipeline([
            ('vectorizer', CountVectorizer(ngram_range=ngram_range)),
            ('classifier', MultinomialNB(alpha=laplace))
        ])
        classifiers.append(('clf_{}'.format(str(ngram_range)), clf))

    # Create the ensemble model using VotingClassifier
    ensemble_classifier = VotingClassifier(classifiers, voting='hard')

    # Train the ensemble model
    ensemble_classifier.fit(X_train, y_train)

    # Evaluate on the test set
    y_pred = ensemble_classifier.predict(X_test)

    # Evaluate the performance
    accuracy = accuracy_score(y_test, y_pred)
    print('Accuracy: {:.4f}'.format(accuracy))



    # # save X_test and y_pred y_test to csv
    # df = pd.DataFrame({'X_test': X_test, 'y_pred': y_pred, 'y_test': y_test})
    # df.to_csv('backend/data/predictions.csv', index=False)

    # # save the model to disk
    # filename = 'finalized_model.sav'
    # pickle.dump(ensemble_classifier, open(filename, 'wb'))
    return ensemble_classifier


def load_model():
    # load the model from disk
    filename = 'finalized_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    return loaded_model

def predict(strings, loaded_model):
    # clean strings remove all non-alphanumeric characters and replace with a ""
    strings = clean_strings(strings)
    result = loaded_model.predict(strings)
    return result


if(__name__ == "__main__"):
    X, y = load_data()
    fit(X, y)

    strings = ["I wish you die", "He's a great guy but his teaching style isnt great. He offers no good material that helps with labs, which are so time consuming and take dozens of hours to finish. Exams were ok but the labs really makes you wish you were studying Computer Science instead of Computer Engineering because it is worse than TORture (pun intended, if you know you know)", "I am sad", "very bad very bad very bad very bad very bad very bad very bad very bad very bad very bad"]

    model = load_model()
    result = predict(strings, model)
    print(result)   


    

    