from flask import Flask, redirect, render_template, request, session
from flask_session import Session
import sqlite3

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = sqlite3.connect("database", check_same_thread=False)
cursor = db.cursor()

@app.route("/")
def index():
    books = db.execute("SELECT * FROM books")
    return render_template("books.html", books=books)

@app.route("/cart", methods=["GET", "POST"])
def cart():
    # Ensure cart exists
    if "cart" not in session:
        session["cart"] = []
    
    # POST
    if request.method == "POST":
        id = request.form.get("id")
        if id:
            session["cart"].append(id)
        return redirect("/cart")
    
    # GET
    searches = "?" + (", ?") * (len(session["cart"]) - 1)
    books = cursor.execute(f"SELECT * FROM books WHERE id IN ({searches})", session["cart"])
    count = GetRepeats(session["cart"])
    return render_template("cart.html", books=zip(books, count))

@app.route("/clear")
def clear():
    session["cart"] = []
    return redirect("/")


def GetRepeats(arr):
    r = {}
    for l in arr:
        if l in r:
            r[l] += 1
        else:
            r[l] = 1

    return list(r.values())


