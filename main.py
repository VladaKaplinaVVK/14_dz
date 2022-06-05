import sqlite3
from collections import Counter


def execute_query(query):
    with sqlite3.connect('netflix.db') as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()
    return result


def get_movie_title(title):
    with sqlite3.connect('netflix.db') as connection:
        cur = connection.cursor()
        query = (f"""
               SELECT title, country, release_year, listed_in, description
               FROM netflix
               where title like '%{title}%'
               order by  release_year desc
               limit 1
           """)

        cur.execute(query)
        result = cur.fetchone()
        return {
            "title": result[0],
            "country": result[1],
            "release_year": result[2],
            "genre": result[3],
            "description": result[4]
        }


def get_movie_release_year(year1, year2):
    query = (f"""
             SELECT title,release_year
             FROM netflix
             where release_year between {year1} and {year2}
             limit 100
     """)
    result = execute_query(query)
    result_list = []
    for row in result:
        result_list.append({"title": row[0],
                            "release_year": row[1]})
    return result_list


def get_movie_rating(rating):
    rating_parameters = {
            "children": "'G'",
            "family": "'G', 'PG', 'PG-13'",
            "adult": "'NC-17', 'R'"
        }
    if rating not in rating_parameters:
        return "Нет указанной категории"
    query = (f"""
                 SELECT title,rating, description
                 FROM netflix
                 where rating in ({rating_parameters[rating]})
         """)
    result = execute_query(query)
    result_list = []
    for row in result:
        result_list.append({"title": row[0],
                            "rating": row[1],
                            "description": row[2]})
    return result_list


def get_movie_genre(genre):
    query = (f"""
             SELECT title, description
             FROM netflix
             where listed_in like '%{genre}%'
             order by release_year desc
             limit 10
     """)
    result = execute_query(query)
    result_list = []
    for row in result:
        result_list.append({"title": row[0],
                            "description": row[1]})
    return result_list


def get_movie_by_actor_partners(actor1, actor2):
    query = (f"""
             SELECT 'cast'
             FROM netflix
             where 'cast' like '%{actor1}%'
             and 'cast' like '%{actor2}%'
     """)
    result = execute_query(query)
    actor_list = []
    for cast in result:
        actor_list.extend(cast[0].split(', '))
    counter = Counter(actor_list)
    result_list = []
    for actor, count in counter.items():
        if actor not in [actor1, actor2] and count > 2:
            result_list.append(actor)
    return result_list



def get_movie_by_parameters(move_type, realise_year, genre):
    query = (f"""
             SELECT type, description
             FROM netflix
             where type = '{move_type}'
             and release_year = {realise_year}
             and listed_in like '%{genre}%'

     """)
    result = execute_query(query)
    result_list = []
    for show in result:
        result_list.append({'title': show[0],
                            'description': show[1]})
    return result_list


