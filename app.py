import sqlite3 as sql

from flask import Flask, flash, render_template, request, url_for, redirect, abort

app = Flask(__name__)


def music_db():
    """
    Open connection to database
    """
    conn = sql.connect(
        "/home/ben/Desktop/Just-IT/python/my-music/music.db"
        )
    conn.row_factory = sql.Row
    return conn

"""
Defining routes
"""
@app.route("/")
@app.route("/home")
def home():
    """
    Rendering the home page
    """
    return render_template("home.html", title="Home")

@app.route("/about")
def about():
    """
    Rendering the about page
    """
    return render_template("about.html", title="About")

@app.route("/add-songs", methods=["GET", "POST"])
def add_songs():
    if request.method == "POST":
        title = request.form["Title"]
        artist = request.form["Artist"]
        genre = request.form["Genre"]
        conn = music_db()
        cursor = conn.cursor()
        song_id = cursor.lastrowid
        cursor.execute("INSERT INTO songs VALUES (?, ?, ?, ?)", (song_id, title, artist, genre))
        conn.commit()
        conn.close()
        return redirect(url_for("songs"))
    return render_template("add-songs.html", title="Add Songs")

@app.route("/songs")
def songs():
    cursor = music_db().cursor()
    cursor.execute("SELECT * FROM songs")
    get_songs = cursor.fetchall()
    
    return render_template("songs.html", title="Songs", get_songs=get_songs)

def get_song(record_id):
    """
    Fetch one unique song record from the database.
    """
    conn = music_db()
    cursor = conn.cursor()
    song = cursor.execute("SELECT * FROM songs WHERE SongID = ?", (record_id,)).fetchone()
    conn.close()
    if song is None:
        abort(404)
    return song


@app.route("/<int:song_id>/update", methods=["GET", "POST"])
def update(song_id):
    """
    Update one record's fields.
    """
    song_record = get_song(song_id)
    if request.method == "POST":
        title = request.form["Title"]
        artist = request.form["Artist"]
        genre = request.form["Genre"]
        
        conn = music_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE songs SET Title = ?, Artist = ?, Genre = ? WHERE SongID = ?", (title, artist, genre, song_id))
        conn.commit()
        conn.close()
        return redirect(url_for("songs"))

    return render_template("update-songs.html", title="Update Songs", song_record=song_record)


if __name__ == "__main__":
    app.run(debug=True, port=8124)
