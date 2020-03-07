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
from tabulate import tabulate
from time import sleep
import requests

from flask_cors import CORS, cross_origin


app = Flask(__name__)


cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/api')
def tweets(label=None):
    url = "http://chuachinhon.pythonanywhere.com"

    option = webdriver.ChromeOptions()
    option.add_argument("--window-size=1920,1080")
    option.add_argument("--disable-extensions")
    option.add_argument("--proxy-server='direct://'")
    option.add_argument("--proxy-bypass-list=*")
    option.add_argument("--start-maximized")
    option.add_argument("--headless")
    option.add_argument("--disable-gpu")
    option.add_argument("--disable-dev-shm-usage")
    option.add_argument("--no-sandbox")
    option.add_argument("--ignore-certificate-errors")
    option.add_argument("--incognito")

    option.add_argument(
        "user-agent= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'")
    path = 'scrape.png'

    driver = webdriver.Chrome(
        executable_path='chromedriver', chrome_options=option)
    hashtag = request.args.get('hashtag')

    try:
        f = open(f"{hashtag}_hashtag.json", encoding='utf-8', errors='ignore')
        data = json.load(f)
        return jsonify(data)

    except FileNotFoundError:
        consumer_key = ''
        consumer_secret = ''
        access_token_key = ''
        access_token_secret = ''

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
            # driver.implicitly_wait(30)
            driver.get(url)
            search = driver.find_element_by_xpath(
                '/html/body/div[1]/form/textarea')
            text = i["tweet"].split(" ")
            cleaned_text = [t.lower() for t in text if(t.isalpha())]
            search.send_keys(' '.join(cleaned_text))
            submit = driver.find_element_by_class_name('btn-info')
            submit.click()
            # sleep(1)
            result = driver.find_element_by_xpath('/html/body/div/p')
            if(result.text == "Real tweet"):
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
    url = "http://chuachinhon.pythonanywhere.com"

    option = webdriver.ChromeOptions()
    option.add_argument("--window-size=1920,1080")
    option.add_argument("--disable-extensions")
    option.add_argument("--proxy-server='direct://'")
    option.add_argument("--proxy-bypass-list=*")
    option.add_argument("--start-maximized")
    option.add_argument("--headless")
    option.add_argument("--disable-gpu")
    option.add_argument("--disable-dev-shm-usage")
    option.add_argument("--no-sandbox")
    option.add_argument("--ignore-certificate-errors")
    option.add_argument("--incognito")

    option.add_argument(
        "user-agent= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'")
    path = 'scrape.png'

    driver = webdriver.Chrome(
        executable_path='chromedriver', chrome_options=option)
    username = request.args.get('username')

    try:
        f = open(f"{username}_username.json",
                 encoding='utf-8', errors='ignore')
        data = json.load(f)
        return jsonify(data)

    except:

        consumer_key = ''
        consumer_secret = ''
        access_token_key = ''
        access_token_secret = ''
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
            driver.get(url)
            search = driver.find_element_by_xpath(
                '/html/body/div[1]/form/textarea')
            obj['tweet'] = i
            obj['id'] = index
            text = i.split(" ")
            cleaned_text = [t.lower() for t in text if(t.isalpha())]
            search.send_keys(' '.join(cleaned_text))
            submit = driver.find_element_by_class_name('btn-info')
            submit.click()
            # sleep(1)
            result = driver.find_element_by_xpath('/html/body/div/p')
            if(result.text == "Real tweet"):
                obj["is_troll"] = 0
            else:
                obj["is_troll"] = 1

            sleep(1)

            data.append(obj)

        with open(f"{username}_username.json", 'w', encoding='utf-8', errors='ignore') as f:

            json.dump(data, f, ensure_ascii=False, indent=4)

    return jsonify(data)


if __name__ == '__main__':
    app.run()
