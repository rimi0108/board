from .models       import Posting
from users.models  import User

from django.test   import TestCase
from django.test   import Client
from unittest.mock import patch, MagicMock

class PostingTest(TestCase):
    def setup(self):
        User.objects.create(
            id      = 1,
            name    = "최혜림",
            email   ="rimi1234@gmail.com",
            password="abcd1234!"
        )
        
    def tearDown(self):
        User.objects.all().delete()
        Posting.objects.all().delete()
        
    def test_post_list_success(self):
        client   = Client()
        response = client.get('/posts?page=1')

        self.assertEqual(response.json(), 
            {
                "POST_LIST": [
                ],
                "page": "1"
            }
        )
        self.assertEqual(response.status_code, 200)
