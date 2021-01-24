from django.test import TestCase, Client #Client 추가
from bs4 import BeautifulSoup
from .models import Post

# Create your tests here.
class TestView(TestCase):
    def setUp(self):
        self.client=Client()

    def test_post_list(self):
        response=self.client.get('/blog/')
        self.assertEqual(response.status_code,200)
        soup=BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text,'Blog')
        navbar=soup.nav
        self.assertIn('Blog',navbar.text)
        self.assertIn('About Me',navbar.text)
        self.assertEqual(Post.objects.count(),0)
        #귀찮으니까 나중에 공부하자.

