import os
from django.core import management
from django.core.management.base import BaseCommand, CommandError

from toolshare.db_helper import fill_database, set_admin_pw

class Command(BaseCommand):
    args = '<none>'
    help = 'Creates/Fills the database with demo data (OVERWRITES db.sqlite3)'

    def handle(self, *args, **options):
        # Purge the old database
        if os.path.isfile('db.sqlite3'):
            print('Removing old db.sqlite3 file...')
            os.remove('db.sqlite3')
        
        # re-initialize the db
        management.call_command('migrate')
        management.call_command('createsuperuser', username='admin', email='admin@toolshare.com', interactive=False )
        
        # set the pw for admin
        set_admin_pw('admin')
        
        # finally, load our default data        
        fill_database()
        print('Demo data loaded successfully.')
