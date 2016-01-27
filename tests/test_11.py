from django.test import TransactionTestCase

from toolshare.models import TSUser

class T(TransactionTestCase):
	def test_do_fail_login(self):
		# create a fake user for testing purposes
		TSUser.createTSUser( username='tester', email='test@test.com', password='tester', address='RIT', name='the tester', zipcode='14623' )

		response = self.client.post('/toolshare/login', {'username':'tester', 'password':'123'})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'invalid password')
