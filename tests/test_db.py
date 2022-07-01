import unittest

from peewee import *

from app import TimelinePost

MODELS= [TimelinePost]

test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS, bind_refs = False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)

        test_db.close()

    def test_timeline_post(self):
        first_post = TimelinePost.create(name='John Doe', email='john@example.com', content = 'Hello World, I \'m John!' )
        assert first_post.id == 1
        second_post = TimelinePost.create(name='Jane Doe', email ='jame@example.com', content='Hello World, I\'m Jane!' )
        assert second_post.id == 2

        stuff = TimelinePost.select().order_by(TimelinePost.created_at.desc())
        
        assert stuff[0].name == 'Jane Doe'
        assert stuff[0].email == 'jame@example.com' 
        assert stuff[0].content == 'Hello World, I\'m Jane!' 
        assert stuff[1].name == 'John Doe'
        assert stuff[1].email == 'john@example.com' 
        assert stuff[1].content == 'Hello World, I \'m John!'
    