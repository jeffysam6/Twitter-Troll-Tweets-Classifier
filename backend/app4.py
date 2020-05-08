from flask import Flask, request, jsonify
import tweepy
import twitter
import json
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
from time import sleep
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from flask_cors import CORS, cross_origin


app = Flask(__name__)


cors = CORS(app, resources={r"/*": {"origins": "*"}})

consumer_key = 'K6D0IcUdlj9tVrMxLNDAV0hbn'
consumer_secret = 'wgLc9Z169OHtqcImHhThA26kjN2C5T5tzxXoltcycScnnuY0uq'
access_token_key = '2193965911-qwngATgg5nhhlDCSPQeJHc79kuEQsKUkhyAjeyJ'
access_token_secret = '19YvZ9ZEk6rQfdduZQoVXSTfYGDdJObFXvxgizFXUEZQn'

df = pd.read_json('../dataset.json',lines=True)
for index,row in df.iterrows():
    # print(index,row)
    df.at[index,'annotation'] = df.at[index,'annotation']['label'][0]

df = df.drop(columns=['extras'])

y = df['annotation']

X_train,X_test,y_train,y_test = train_test_split(df['content'],y,test_size=0.33,random_state=53,shuffle = True)

count_vectorizer = CountVectorizer(stop_words = 'english')

count_train = count_vectorizer.fit_transform(X_train)

loaded_model = pickle.load(open('../count_model.sav', 'rb'))

@app.route('/api')
def tweets(label=None):


    hashtag = request.args.get('hashtag')

    try:
        f = open(f"{hashtag}_hashtag.json", encoding='utf-8', errors='ignore')
        data = json.load(f)
        return jsonify(data)

    except FileNotFoundError:

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        api = tweepy.API(auth)

        data = []
 
        for i, tweet in enumerate(tweepy.Cursor(api.search, q=f"#{hashtag}", rpp=100).items()):
            obj = {}
            obj['id'] = i+1
            obj["tweet"] = tweet.text
            obj['name'] = tweet.user.name
            obj['username'] = tweet.user.screen_name

            data.append(obj)

            if(len(data) == 25):
                break

        for i in data:
            
            text = i["tweet"].split(" ")
            # print(text)
            cleaned_text = [t.lower() for t in text if(t.isalpha())]
            vec = count_vectorizer.transform([' '.join(cleaned_text)])
            predict = loaded_model.predict(vec)
            
            if(predict[0] == "0"):
                i["is_troll"] = 0
            else:
                i["is_troll"] = 1

            sleep(1)

        with open(f"{hashtag}_hashtag.json", 'w', encoding='utf-8', errors='ignore') as f:

            json.dump(data, f, ensure_ascii=False, indent=4)
        # driver.implicitly_wait(50)

    return jsonify(data)


@app.route('/user')
def users(label=None):

    username = request.args.get('username')
    try:
        f = open(f"{username}_username.json",
                 encoding='utf-8', errors='ignore')
        data = json.load(f)
        return jsonify(data)
    
    except:

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token_key, access_token_secret)
        api = tweepy.API(auth)

        number_of_tweets = 10

        tweets = api.user_timeline(screen_name=username)
        tweets_for_csv = [tweet.text for tweet in tweets]

        temp_data = []
        data = []

        for i in tweets_for_csv:
            temp_data.append(i)

        for index, i in enumerate(temp_data):
            obj = {}
            obj['tweet'] = i
            obj['id'] = index
            text = i.split(" ")
            cleaned_text = [t.lower() for t in text if(t.isalpha())]
            # print(cleaned_text)
            vec = count_vectorizer.transform([' '.join(cleaned_text)])
            predict = loaded_model.predict(vec)
            if(predict[0] == "0"):
                obj["is_troll"] = 0
            else:
                obj["is_troll"] = 1


            data.append(obj)

        with open(f"{username}_username.json", 'w', encoding='utf-8', errors='ignore') as f:

            json.dump(data, f, ensure_ascii=False, indent=4)

    return jsonify(data)


if __name__ == '__main__':
    app.run()
