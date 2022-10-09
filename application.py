from flask import Flask, redirect, render_template, request, session
from flask_session import Session
import sqlite3

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = sqlite3.connect("database", check_same_thread=False)

@app.route("/")
def index():
    books = db.execute("SELECT * FROM books")
    return render_template("books.html", books=books)

@app.route("/cart", methods=["GET", "POST"])
def cart():
    # books = db.execute("SELECT * FROM books")
    # return render_template("books.html", books=books)
    return null