from flask import Flask, flash, render_template, request, url_for, redirect, abort

app = Flask(__name__)

"""
Home route
"""
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title="Home")

@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/add-songs")
def add_songs():
    return render_template("add-songs.html", title="Add Songs")

@app.route("/songs")
def songs():
    return render_template("songs.html", title="Songs")

if __name__ == "__main__":
    app.run(debug=True, port=8124)
