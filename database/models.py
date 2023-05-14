import os
from sqlalchemy import DATE, Column, ForeignKey, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

#database_name = 'castingagency'
#DB_USER = os.getenv('DB_USER', 'postgres')
#DB_PASSWORD = os.getenv('DB_PASSWORD', 'abc')
#database_path = 'postgresql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD,'localhost:5432', database_name)

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


class Actor(db.Model):
    __tablename__ = "actors"
    id = Column(Integer(), primary_key=True)
    name = Column(String(512), nullable=False)
    gender = Column(String(10), nullable=False)
    date_of_birth = Column(DATE, nullable=False)

    def __init__(self, name, gender, date_of_birth):
        self.name = name
        self.gender = gender
        self.date_of_birth = date_of_birth

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def short(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def detailed_info(self):
        return {
            "name": self.name,
            "gender": self.gender,
            "date_of_birth": self.date_of_birth.strftime("%B %d, %Y")
        }

    def __repr__(self):
        json.dumps(self.short())

    def getActorById(id):
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        return actor 

actor_of_movie = db.Table(
    'actor_of_movie',
    Column('actor_id', Integer, ForeignKey('actors.id'), primary_key=True),
    Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True)
)

class Movie(db.Model):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(DATE, nullable=False)
    cast = db.relationship('Actor', secondary=actor_of_movie,
                           backref=db.backref('movies', lazy=True))

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def short(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date
        }

    def detailed_info(self):
        return {
            "title": self.title,
            "release_date": self.release_date,
            "cast": [actor.name for actor in self.cast]
        }

    def __repr__(self):
        return json.dumps(self.short())
    
    def getMovieById(id):
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        return movie 
    


