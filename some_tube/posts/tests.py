from django.test import TestCase, Client

from posts.models import Group, User, Post


class TestIndex(TestCase):
    def setUp(self):
        self.non_auth_client = Client()
        self.auth_client = Client()
        user = User.objects.create(
            username='test_user',
            email='a@a.com'
        )
        user.set_password('123')
        user.save()
        self.auth_client.login(username='test_user', password='123')
        Group.objects.create(
            title='test',
            slug='test',
            description='some_test_description'

        )

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        response = self.auth_client.get('/test_user/')
        self.assertEqual(response.status_code, 200)

    def test_group(self):
        response = self.client.get(f'/group/test')
        self.assertEqual(response.status_code, 200)

    def test_create_new_post(self):
        post_response = self.auth_client.post("/new/", data={
            'text': 'hello world',
            'group': 1
        })
        self.assertTrue(
            Post.objects.filter(text='hello world', group=1).exists()
        )
        self.assertEqual(post_response.url, '/')

    def test_redirects_non_auth_client(self):
        response = self.non_auth_client.post("/new/", data={
            'text': 'hello world',
            'group': 1
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/auth/login/?next=/new/')

    def test_update_post(self):
        self.auth_client.post("/new/", data={
            'text': 'hello world',
            'group': 1
        })
        self.assertTrue(
            Post.objects.filter(text='hello world', group=1).exists()
        )
        update_response = self.auth_client.post('/test_user/1/edit/', data={'text': 'updated post'})
        self.assertTrue(
            Post.objects.filter(text='updated post').exists()
        )
        self.assertEqual(update_response.url, '/test_user/1')

