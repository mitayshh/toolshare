from django.test import SimpleTestCase

class T(SimpleTestCase):
	def test_do_unknown_login(self):
		response = self.client.post('/toolshare/login', {'username':'jjsmith', 'password':'123abc'})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'unknown user')
