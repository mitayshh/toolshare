from django.test import TransactionTestCase

from toolshare.models import TSUser

class T(TransactionTestCase):
	def test_do_successful_login(self):
		# create a fake user for testing purposes
		TSUser.createTSUser( username='tester', email='test@test.com', password='tester', address='RIT', name='the tester', zipcode='14623' )

		# finally, attempt a login!
		response = self.client.post('/toolshare/login', {'username':'tester', 'password':'tester'})
		self.assertRedirects(response, '/toolshare/zone')
