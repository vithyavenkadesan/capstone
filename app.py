import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from database.models import db_drop_and_create_all, setup_db, Actor, Movie
from auth.auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  with app.app_context():
    db_drop_and_create_all()

  # ROUTES
  @app.route('/actors', methods=['GET'])
  @requires_auth("get:actors")
  def get_actors(payload):
      query_results = Actor.query.order_by(Actor.id).all()
      actors = [actor.short() for actor in query_results]

      return jsonify({
            "success": True,
            "actors": actors
        }), 200
  
  @app.route('/actors/<int:actor_id>')
  @requires_auth("get:actor-detail")
  def get_actor_by_id(payload, actor_id):
      actor = Actor.getActorById(actor_id)
      if actor is None:
        abort(404)
      return jsonify({
            "success": True,
            "actor": actor.detailed_info()
        }), 200
  
  @app.route('/movies', methods=['GET'])
  @requires_auth("get:movies")
  def get_movies(payload):
      query_results = Movie.query.order_by(Movie.id).all()
      actors = [movie.short() for movie in query_results]

      return jsonify({
            "success": True,
            "movies": actors
        }), 200
  
  @app.route('/movies/<int:movie_id>')
  @requires_auth("get:movie-detail")
  def get_movie_by_id(payload, movie_id):
      movie = Movie.getMovieById(movie_id)
      if movie is None:
        abort(404)
      return jsonify({
            "success": True,
            "movie": movie.detailed_info()
        }), 200
  

  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def create_actor(payload):
        body = request.get_json()
        new_name = body.get("name", None)
        new_gender = body.get("gender", None)
        new_dob = body.get("dob", None)
        try:
            actor = Actor(name=new_name, gender=new_gender, date_of_birth=new_dob)
            actor.insert()
            created_drink = [actor.detailed_info()]
            return jsonify(
                {
                    "success": True,
                    "actors": created_drink
                }
            )

        except:
            print(sys.exc_info())
            abort(500)

  @app.route('/actors/<id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actor(payload, id):
        body = request.get_json()
        new_name = body.get("name", None)
        new_gender = body.get("gender", None)
        new_dob = body.get("dob", None)
        try:
            actor = Actor.getActorById(id)
            if actor is None:
                abort(404)
            if new_name:
                actor.name = new_name
            if new_gender:
                actor.gender =  new_gender
            if new_dob:
                actor.date_of_birth =  new_dob
            actor.update()
            updated_actor = [actor.detailed_info()]
            return jsonify(
                {
                    "success": True,
                    "actors": updated_actor
                }
            )

        except:
            print(sys.exc_info())
            abort(500)

  @app.route('/actors/<id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(payload, id):
        try:
            actor = Actor.getActorById(id)
            if actor is None:
                abort(404)
            actor.delete()
            return jsonify(
                {
                    "success": True,
                    "delete": id
                }
            )

        except:
            print(sys.exc_info())
            abort(500)

  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def create_movie(payload):
        body = request.get_json()
        new_title = body.get("title", None)
        new_release_date = body.get("release_date", None)
        try:
            movie = Movie(title=new_title, release_date=new_release_date)
            movie.insert()
            created_movie = [movie.detailed_info()]
            return jsonify(
                {
                    "success": True,
                    "movies": created_movie
                }
            )

        except:
            print(sys.exc_info())
            abort(500)

  @app.route('/movies/<id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movie(payload, id):
        body = request.get_json()
        new_title = body.get("title", None)
        new_release_date = body.get("release_date", None)
        try:
            movie = Movie.getMovieById(id)
            if movie is None:
             abort(404)
            if new_title:
                movie.title = new_title
            if new_release_date:
                movie.release_date =  new_release_date
          
            movie.update()
            updated_movie = [movie.detailed_info()]
            return jsonify(
                {
                    "success": True,
                    "movies": updated_movie
                }
            )

        except:
            print(sys.exc_info())
            abort(500)

  @app.route('/movies/<id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(payload, id):
        try:
            movie = Movie.getMovieById(id)
            if movie is None:
                abort(404)
            movie.delete()
            return jsonify(
                {
                    "success": True,
                    "delete": id
                }
            )

        except:
            print(sys.exc_info())
            abort(500)
  # Error Handling

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

  @app.errorhandler(404)
  def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal error"
    }), 500

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400

  @app.errorhandler(401)
  def unauthorised(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorised"
    }), 401

  @app.errorhandler(403)
  def forbidden(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "Forbidden"
    }), 403


  return app

APP = create_app()
if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=5000, debug=True)

