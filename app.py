from unittest import main

from flask import Flask, jsonify
from main import *

app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False


@app.route('/movie/<title>')
def get_by_movie_title_catalog(title):
    return jsonify(get_movie_title(title))


@app.route('/movie/<int:year1>/to/<int:year2>')
def get_movie_by_release_year_catalog(year1, year2):
    return jsonify(get_movie_release_year(year1, year2))


@app.route('/rating/<category>')
def get_movie_by_rating_catalog(category):
    return jsonify(get_movie_rating(category))


@app.route('/genre/<genre>')
def get_movie_by_genre_catalog(genre):
    return jsonify(get_movie_genre(genre))


if __name__ == '__main__':
    app.run(debug=True)
