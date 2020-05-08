from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

df = pd.read_json('./dataset.json',lines=True)

# def clean(x):
#     return x['label'][0]

# df['annotation'] = df['annotation'].apply(clean)
# print(df.head())
for index,row in df.iterrows():
    # print(index,row)
    df.at[index,'annotation'] = df.at[index,'annotation']['label'][0]
    
df = df.drop(columns=['extras'])

# print(df.columns)
    
y = df['annotation']

X_train,X_test,y_train,y_test = train_test_split(df['content'],y,test_size=0.33,random_state=53,shuffle = True)

count_vectorizer = CountVectorizer(stop_words = 'english')

count_train = count_vectorizer.fit_transform(X_train)

# count_test = count_vectorizer.transform(X_test)


# print(count_vectorizer.get_feature_names()[:10])

# nb_classifier = MultinomialNB()

# nb_classifier.fit(count_train,y_train)

# pred = nb_classifier.predict(count_test)

# score = metrics.accuracy_score(y_test,pred)
# print("Count vec",score)

# pickle.dump(nb_classifier, open('count_model.sav', 'wb'))


loaded_model = pickle.load(open('count_model.sav', 'rb'))
# result = loaded_model.score(count_test, y_test)
# print(result)

vec = count_vectorizer.transform(["You are so nice fuck"])

predict = loaded_model.predict(vec)
print(predict)
###########
# tfidf_vectorizer = TfidfVectorizer(stop_words="english",max_df=0.7)

# tfidf_train = tfidf_vectorizer.fit_transform(X_train)

# tfidf_test = tfidf_vectorizer.transform(X_test)

# nb_classifier = MultinomialNB()

# nb_classifier.fit(tfidf_train,y_train)

# pred = nb_classifier.predict(tfidf_test)

# score = metrics.accuracy_score(y_test,pred)
# print("tfidf",score)