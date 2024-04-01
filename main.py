import requests
from bs4 import BeautifulSoup
from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
import json


app =Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] ="sqlite:///movies.db"
db= SQLAlchemy()
db.init_app(app)


class Movieclass(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    movie_name=db.Column(db.String(140))

with app.app_context():
    db.create_all()



URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

# Write your code below this line 👇

responce = requests.get(URL)
website_html = responce.text

soup = BeautifulSoup(website_html,"html.parser")
# print(soup.prettify())

all_movie = soup.find_all(name="h3" ,class_="title")
# print(all_movie)

movie_titles = [movie.getText() for movie in all_movie]
# print(movie_titles)
movies=movie_titles[::-1]
# print(movies)

json_data = json.dumps(movies)
# print(json_data)



    


with open("movies.txt",mode = "w",encoding="utf-8") as file:
    for movie in movies:
        file.write(f"{movie}\n")


@app.route("/movies",methods=["POST"])
def all_movie():
    data = json.loads(json_data)

    # id = dict.get("new_id")
    # movie_name=dict.get("movie")

    # entry = Movies(id = id ,movie=movie_name)
    # db.session.add(entry)
    # db.session.commit()

    # print(type(data))
    data_list=[]
    for index ,movie in enumerate(data):

        dict={
            "id":index,
            "movie_name":movie
        }
    
        data_list.append(dict)
        id = dict.get("id")
        movie_name=dict.get("movie")

        entry = Movieclass(id = id ,movie_name=movie)
        db.session.add(entry)
        db.session.commit()
    # print(data_list)
    
    
    return jsonify(data_list)


@app.route("/get_movies",methods=["GET"])
def getmovies():
    getmovies = Movieclass.query.all()
    # print(getmovies)
    new_list=[]
    for new_movies in getmovies:
        # print(new_movies)
        new_list.append({"id":new_movies.id,"movie":new_movies.movie_name})

        print(new_list)
    
    return jsonify(new_list)


@app.route("/get_movies/<int:movie_id>",methods=["GET"])
def movies_id(movie_id):
    getmovies = Movieclass.query.get(movie_id)
    movie_data=({"id":getmovies.id,"movie":getmovies.movie_name})

    return jsonify(movie_data)


@app.route("/update_movie/<int:movie_id>",methods=["PUT"])
def update(movie_id):
    getmovies = Movieclass.query.get(movie_id)
    a = json.loads(request.data)
    print(a)

    movie=a.get("movie")
    getmovies.movie_name=movie
    db.session.commit()
    new_data=({"id":getmovies.id,"movie":getmovies.movie_name})


    return jsonify(new_data)

@app.route("/delete_movie/<int:movie_id>",methods=["DELETE"])
def deletemovie(movie_id):
    getmovies = Movieclass.query.get(movie_id)
    
    db.session.delete(getmovies)
    db.session.commit()

    return jsonify("deleted successfully")












if __name__ == "__main__":
    app.run(debug=True) 







