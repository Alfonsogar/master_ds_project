import time
import requests
import json
import csv


def filter_tmbd_json(json_data, movieid):
    tmdb_dict = {"movieid": movieid}
    for key in json_data.keys():
        if key in flat_keys:
            # print key, json_data[key]
            tmdb_dict[key] = json_data[key]
        elif key in nested_keys_name:
            nested_keys_list = []
            for i in range(0, len(json_data[key])):
                # print key, json_data[key][i]["name"]
                nested_keys_list.append({"name": json_data[key][i]["name"]})
            tmdb_dict[key] = nested_keys_list
    return tmdb_dict


# open file links and load tmdb id list to movies
movies = []
# movieid, imdbid, tmdbid
with open("clean_links.csv", 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        movies.append(row)

flat_keys = ["popularity", "budget", "vote_average", "runtime", "id", "revenue"]
nested_keys_name = ["production_countries"]



# 40 requests every 10 seconds
i = 0
t = time.time()

movies = movies[0:]
movies_json = []

qty = len(movies)
for id in movies:
    print (str(qty) + ': ' + id[1])
    qty-=1

    if i > 39:
        i = 0
        t = time.time()
    if i == 39 and (time.time() - t) < 10:
        time.wait(10 - (time.time() - t) + 1)

    url = "https://api.themoviedb.org/3/movie/" + str(
        id[2]) + "?api_key=63f97a523659b7cb44849bfcb1759540"
    response = requests.get(url)
    i += 1
    if (response.ok):
        movies_json.append(filter_tmbd_json(response.json(), id[0]))
        # else:
        # 	response.raise_for_status()

with open("tmdb_movies.json", 'w') as file:
    for movie in movies_json:
        json.dump(movie, file)
        file.write('\n')
    # json.dump(movies_json, fp, indent=2)

    # my_dict = {
    #	"production_countries":{"name":"United States of America"},
    #	"revenue":373554033,
    #	"overview":"lala",
    #	"keywords":{"keywords":{"name":"jealousy"}},
    #	"id":862,
    #	"genres":{"name":"Animation"},
    #	"title":"Toy Story",
    #	"homepage":"http://toystory.disney.com/toy-story",
    #	"status":"Released",
    #	"spoken_languages":{"name":"English"},
    #	"imdb_id":"tt0114709",
    #	"cast":{
    #			 "name":"Tom Hanks",
    #			 "gender":2,
    #			 "character":"Woody (voice)"
    #			 "order":0
    #	},
    #	"crew":{
    #			 "name":"Tom Hanks",
    #			 "department":"Actors",
    #			 "job":"Voice"
    #		  }
    #	},
    #	"production_companies":{"name":"Pixar Animation Studios"},
    #	"release_date":"1995-10-30",
    #	"popularity":18.431762,
    #	"original_title":"Toy Story",
    #	"budget":30000000,
    #	"vote_average":7.8,
    #	"runtime":81
    # }
