from django.test import SimpleTestCase

class T(SimpleTestCase):
    # we use chaining to redirect / to /toolshare to /toolshare/home
    def test_index(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/toolshare', status_code=302, target_status_code=301)

        response = self.client.get('/toolshare')
        self.assertRedirects(response, '/toolshare/', status_code=301)

        response = self.client.get('/toolshare/home')
        self.assertEqual(response.status_code, 200)
