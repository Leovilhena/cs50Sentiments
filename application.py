from flask import Flask, redirect, render_template, request, url_for

import helpers
import os
import sys
from analyzer import Analyzer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    # validate screen_name
    screen_name = request.args.get("screen_name", "").lstrip("@")
    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets
    tweets = helpers.get_user_timeline(screen_name)

    # absolute paths to lists
    positives = os.path.join(sys.path[0], "positive-words.txt")
    negatives = os.path.join(sys.path[0], "negative-words.txt")

    # instantiate analyzer
    analyzer = Analyzer(positives, negatives)
    
    # variables declaration
    score = 0
    
    # for porcentage calculation
    total_score = 0
    positive, negative, neutral = 0.0, 0.0, 0.0
        
    # iterates throught each tweet and print out them colored, up til 100 tweets
    if tweets != None:
        for i in range(100):
            if i >= len(tweets):
                break
            score = analyzer.analyze(tweets[i])
            total_score += 1
            if score > 0.0:
                positive += 1
            elif score < 0.0:
                negative += 1
            else:
                neutral += 1
            
    # percentage calculation, suits if number of tweets is less then 100        
    if total_score == 0:
        neutral = 100
    else:
        if positive != 0:
            positive = (1.0 * positive / total_score) * 100
        if negative != 0:
            negative = (1.0 * negative / total_score) * 100
        if neutral != 0:
            neutral = (1.0 * neutral / total_score) * 100

    # generate chart
    chart = helpers.chart(positive, negative, neutral)

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name)
