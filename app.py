from flask import Flask,request,render_template,redirect
import psycopg2
import os
import time

DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASS"]
DB = os.environ["DB"]
DB_HOST = os.environ["DB_HOST"]

app = Flask(__name__)

def init_tables():

    CREATE_TABLE = "CREATE TABLE IF NOT EXISTS REVIEWS (name TEXT NOT NULL, movname TEXT NOT NULL, rating TEXT NOT NULL, review TEXT NOT NULL)"
    conn = psycopg2.connect(host=DB_HOST,database=DB, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLE)
    conn.commit()
    cursor.close()
    conn.close()

def add_review(name,movname,rating,review):

    ADD_REVIEW = "INSERT INTO REVIEWS (name,movname,rating,review) VALUES (%s,%s,%s,%s)"
    conn = psycopg2.connect(host=DB_HOST,database=DB, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute(ADD_REVIEW,(name,movname,rating,review))
    conn.commit()
    cursor.close()
    conn.close()

def load_reviews():

    reviews = []

    LOAD_REVIEW = "SELECT * from REVIEWS"
    conn = psycopg2.connect(host=DB_HOST,database=DB, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute(LOAD_REVIEW)
    results = cursor.fetchall()

    for row in results:
        reviews.append((row[0],row[1],row[2],row[3]))
    cursor.close()
    conn.close()

    return reviews

@app.route("/reviews/add",methods=["POST"])
def addreview():

    name = request.form["name"]
    movname = request.form["movname"]
    rating = request.form["rating"]
    review = request.form["review"]

    add_review(name,movname,rating,review)

    return {"success":True}

@app.route("/reviews/list",methods=["POST"])
def listreviews():

    reviews = load_reviews()

    return {"success":True,"list":reviews}

time.sleep(20)
init_tables()
app.run(host="0.0.0.0",port=5000)
