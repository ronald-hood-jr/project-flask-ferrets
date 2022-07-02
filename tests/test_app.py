from dataclasses import dataclass
import unittest
import os 
os.environ['TESTING'] = 'true'

from app import app 

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_aboutMe(self):
        response = self.client.get('/')
        assert response.status_code == 200
        response_text = response.get_data(as_text = True)
        assert '<title>Ronald Hood Jr.</title>' in response_text
        assert '<a class="btn" href="/#">Contact Me</a>' in response_text

    def test_timeline(self):
        response = self.client.get('/api/timeline_post')
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert 'timeline_posts' in json
        assert len(json['timeline_posts']) == 0

        #post and get testing
        response = self.client.post('/api/timeline_post', 
        data = {'name':'michelle was here-2', 'email':'michellelam@gmail.com', 'content': 'hi' })
        assert response.status_code == 200

        assert response.is_json
        json = response.get_json()
        assert json['name'] == 'michelle was here-2'

        response = self.client.get('/api/timeline_post')
        json = response.get_json()
        assert 'michelle was here-2' == json['timeline_posts'][0]['name']

        #timeline testing
        response = self.client.get('/timeline')
        response_text = response.get_data(as_text = True)
        assert '<a class="btn btn-ghost normal-case text-xl" href="/">Ronald Hood Jr.</a>' in response_text

    def test_malformed_timeline_post(self):
          #POST request missing name
        response = self.client.post("/api/timeline_post", data=
        {"email": "John@example.com", "content": "Hello World, I'm John"})
        assert response.status_code == 400
        response_text = response.get_data(as_text=True)
        assert "Invalid name" in response_text

        #POST request with empty content
        response = self.client.post("/api/timeline_post", data=
        {"name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        response_text = response.get_data(as_text=True)
        assert "Invalid content" in response_text

        #POST request with malformed email 
        response = self.client.post('/api/timeline_post', data=
        {'name': "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        response_text = response.get_data(as_text=True)
        assert "Invalid email" in response_text