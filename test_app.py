
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.models import setup_db, Actor, Movie


class CastingAgencyTestCase(unittest.TestCase):
    
    def setUp(self):
        DB_USER = os.getenv('DB_USER', 'postgres')
        DB_PASSWORD = os.getenv('DB_PASSWORD', 'abc')
        self.database_name = "castingagency"
        self.database_path = "postgres://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD,'localhost:5432', self.database_name)

        self.assistant_token = os.environ['assistant_token']
        self.director_token = os.environ['director_token']
        self.producer_token = os.environ['producer_token']
        self.app = create_app(self.database_path)
        self.client = self.app.test_client
 
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_actors_failure(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('success'), False)

    def test_get_actors_success(self):
        res = self.client().get('/actors', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)
        self.assertTrue(data.get('actors'))

    def test_get_categories_error(self):
        res = self.client().get('/actorss', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data.get('success'), False)
        self.assertEqual(data.get('message'), 'resource not found')

    def test_get_movies_success(self):
        res = self.client().get('/movies', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)
        self.assertTrue(data.get('movies'))

    def test_get_actor_detail_success(self):
        res = self.client().get('/actors/2', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)
        self.assertTrue(data.get('actor'))

    def test_get_movie_detail_success(self):
        res = self.client().get('/movies/2', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)
        self.assertTrue(data.get('movie'))

    def test_delete_movie_error(self):
        res = self.client().delete('/movies/', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data.get('success'), False)
        self.assertEqual(data.get('message'), 'resource not found')

    def test_delete_movie_auth_error(self):
        res = self.client().delete('/movies/2', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data.get('success'), False)

    def test_delete_actor_error(self):
        res = self.client().delete('/actors/1', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data.get('success'), False)

    def test_create_actor_failure(self):
        requestBody = {
            "name" : "Karthi",
            "gender": "Male",
            "dob": "1989-09-28"
        }
        res = self.client().post('/actors', json=requestBody, headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data.get('success'), False)

    def test_create_actor_success(self):
        requestBody = {
            "name" : "Karthi",
            "gender": "Male",
            "dob": "1989-09-28"
        }
        res = self.client().post('/actors', json=requestBody, headers={
            'Authorization': "Bearer {}".format(self.director_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)
        self.assertGreater(data.get('created'), 0)

    def test_create_movie_failure(self):
        requestBody = {
              "title" : "PS-2",
              "release_date": "2023-04-28"
        }
        res = self.client().post('/movies', json=requestBody, headers={
            'Authorization': "Bearer {}".format(self.director_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data.get('success'), False)
    
    def test_create_movie_failure(self):
        requestBody = {
              "title" : "PS-2",
              "release_date": "2023-04-28"
        }
        res = self.client().post('/movies', json=requestBody, headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)

    def test_create_actor_success(self):
        requestBody = {
            "name" : "Karthi",
            "gender": "Male",
            "dob": "1989-09-28"
        }
        res = self.client().post('/actors', json=requestBody, headers={
            'Authorization': "Bearer {}".format(self.director_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)

    def test_update_movie_failure(self):
        requestBody = {
              "release_date": "2023-04-28"
        }
        res = self.client().patch('/movies/3', json=requestBody, headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data.get('success'), False)
    
    def test_update_movie_success(self):
        requestBody = {
              "release_date": "2023-04-28"
        }
        res = self.client().patch('/movies/2', json=requestBody, headers={
            'Authorization': "Bearer {}".format(self.director_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)

    def test_update_actor_failure(self):
        requestBody = {
               "dob": "1987-09-28"
        }
        res = self.client().patch('/actors/3', json=requestBody, headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data.get('success'), False)
    
    def test_update_actor_success(self):
        requestBody = {
               "dob": "1987-09-28"
        }
        res = self.client().patch('/actors/3', json=requestBody, headers={
            'Authorization': "Bearer {}".format(self.director_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()