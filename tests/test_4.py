from django.test import SimpleTestCase

class T(SimpleTestCase):
	def test_wrongemail_register(self):
		response = self.client.post('/toolshare/register', {'username':'jsmith', 'password':'123abc', 'reTypePassword':'123abc', 'name':'John Smith', 'email':'abc.com', 'address':'123 Abc St', 'zipcode':'14623'})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Enter a valid email address.')
