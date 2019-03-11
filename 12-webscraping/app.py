#!/usr/bin/env python

from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config['MONGO_URI']= "mongodb://localhost:27017/marsdatadb"
mongo = PyMongo(app)


@app.route("/")
def home():
	marsdata = mongo.db.marsdata.find_one()
	return render_template("index.html", marsdata=marsdata)
		

@app.route("/scrape")
def do_scrape():
	marsdata = mongo.db.marsdata
	scraped_data = scrape_mars.scrape()
	marsdata.update(
		{},
		scraped_data,
		upsert=True
	)
	return redirect("/", code=302)
		

if __name__ == "__main__":
    app.run(debug=True)
