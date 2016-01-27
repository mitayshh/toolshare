from django.test import TransactionTestCase

class T(TransactionTestCase):
	def test_register(self):
		response = self.client.post('/toolshare/register', {'username':'jsmith', 'password':'123abc', 'reTypePassword':'123abc', 'name':'John Smith', 'email':'abc@abc.com', 'address':'123 Abc St', 'zipcode':'14623'})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Registered')
