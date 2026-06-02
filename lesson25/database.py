import sqlite3
from fileinput import close

from models import Movie, MovieCreate
from streamlit import title


def create_connection():
    connection = sqlite3.connect("movies.db")
    connection.row_factory = sqlite3.Row
    return connection

def create_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''
       create table if not exists movies(
        id integer primary key autoincrement,
        title text not null,
        director text not null
       )    
    ''')

    connection.commit()
    connection.close()

create_table()

def create_movie(movie: MovieCreate) -> int:
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("insert into movies (title, director) values (?,?)", (movie.titile, movie.director))
    connection.commit()
    movie_id = cursor.lastrowid
    connection.close()
    return movie_id

def read_movies():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("select * from movies")
    rows = cursor.fetchall()
    connection.close()
    movies = [Movie(id=row[0], title=row[1], director=row[2]) for row in rows]
    return movies

def read_movie(movie_id: int):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("select * from movies where id =?", (movie_id))
    row = cursor.fetchone()
    connection.close()
    if row is None:
        return None
    return Movie(id=row["id"], title=row["title"], director=row["director"])

def update_movie(movie_id: int, movie: MovieCreate) -> bool:

    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE movies SET title = ?, director = ? WHERE id = ?", (movie.title, movie.director, movie_id))
    connection.commit()
    updated = cursor.rowcount
    connection.close()
    return updated > 0


def delete_movie(movie_id: int) -> bool:

    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
    connection.commit()
    deleted = cursor.rowcount
    connection.close()
    return deleted > 0

