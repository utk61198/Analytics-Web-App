from flask import Flask,render_template,flash, redirect,url_for,session,logging,request
from flask_sqlalchemy import SQLAlchemy
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import json
from model import tweetObject
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/utkarsh/projects/seproject/database.db'
db = SQLAlchemy(app)
uname_temp=""
passw_temp=""
mail_temp=""
keyword=""
posts=[]
filters_positive=""
filters_negative=""
filters_neutral=""
filters=[]
chartcount=[]
data=[]
consumer_key="Pr3cXzpFUDWFoBQeR45uEZuvN"
consumer_secret="4exOWGmUD1ZVXoCvwOAkafbN6xZlGo7vzrCRpFtb7krYyBc1UP"
access_token="1138374206750482433-EMwDxdGa9fBSyDlyrcpx9eL1TXxAwN"
access_token_secret="XSESA9TX8bnoAR53GQCetWm3vZbV4WORV2zGpTEHOLCWj"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))


@app.route("/",methods=["GET","POST"])
def index():
    return render_template("index.html")


@app.route("/login",methods=["GET","POST"])
def login():
	if request.method=="POST":
		global uname_temp
		global passw_temp
		uname=request.form['uname']
		passw=request.form['passw']
		uname_temp=uname
		passw_temp=passw
		login=user.query.filter_by(username=uname,password=passw).first()
		if login is not None:
			return redirect(url_for("search"))
	return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['email']
        passw = request.form['passw']
        

        register = user(username = uname, email = mail, password = passw)
        db.session.add(register)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/search",methods=["GET","POST"])
def search():
    global keyword
    global posts
    global filters
    global filters_positive
    global filters_negative
    global filters_neutral
    global filters
    global chartcount
    if request.method=="POST":
        chartcount=[]
        filters=[]
        keyword=request.form['keyword']
        filters_positive=request.form.get('choice1')
        filters_negative=request.form.get('choice2')
        filters_neutral=request.form.get('choice3')
        if filters_positive:

           filters.append(filters_positive)
        if filters_negative:
            
           filters.append(filters_negative)
        if filters_neutral:

           filters.append(filters_neutral)

        tweet_object=tweetObject()

        t = []
        tweets = api.search(keyword, tweet_mode='extended')
        pos_count=0
        neg_count=0
        neu_count=0
        for tweet in tweets:

           polarity = TextBlob(tweet.full_text).sentiment.polarity
            
           subjectivity = TextBlob(tweet.full_text).sentiment.subjectivity
           if(polarity>0):
           	sentiment="positive"
           	pos_count=pos_count+1
           elif(polarity<0):
           	sentiment="negative"
           	neg_count=neg_count+1
           else:
           	sentiment="neutral"
           	neu_count=neu_count+1
           if len(filters)==0:
           	t.append([tweet.full_text,sentiment])

           if sentiment in filters:
             t.append([tweet.full_text,sentiment])

        posts=t
        chartcount.append(pos_count)
        chartcount.append(neg_count)
        chartcount.append(neu_count)

        if posts is not None:
           return redirect(url_for("posts"))





    return render_template("search.html")



@app.route("/posts",methods=["GET","POST"])
def posts():
	global posts
	global filters
	return render_template("posts.html",posts=posts,filters=filters)


@app.route("/stats",methods=["GET","POST"])
def stats():
	global chartcount
	global data
	data=chartcount

	return render_template("stats.html",chartcount=data)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)