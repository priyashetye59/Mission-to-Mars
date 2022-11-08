#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping


# In[2]:


app = Flask(__name__)


# In[3]:


# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# In[4]:


@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


# In[5]:


@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update_one({}, {"$set": mars_data}, upsert=True)
    return redirect('/', code=302)


# In[6]:


if (__name__ == "__main__"):
    app.run()


# In[ ]:




