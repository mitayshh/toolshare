from django.contrib.auth.models import User
from toolshare.models import *
from datetime import timedelta
from django.utils import timezone

# to reinit the database... ( remember that 'admin' has 'admin' for the pw! )
# cd SVN/trunk/mysite
# python3 manage.py ts_create_db

def set_admin_pw(password):
    # set the pw for the superuser NON-INTERACTIVELY :)
    su = User.objects.all()[0]
    su.set_password(password)
    su.save()

def create_tool( user, name, location, desc, img ):
    # mangle the img a bit
    img = 'static/images/simpsons/' + img

    return Tool.createTool(owner = user,
                            name = name,
                            loc = location,
                            desc = desc,
                            img = img
    )

# fills the DB with demo stuff
def fill_database():
    create_users()
    create_tools()
    create_borrows()

def create_users():
    homer = TSUser.createTSUser(username='homer', email='homer@simpsons.com', password='homer', address='742 Evergreen Terrace', name='Homer Simpson', zipcode='62701')
    marge = TSUser.createTSUser(username='marge', email='marge@simpsons.com', password='marge', address='742 Evergreen Terrace', name='Marge Simpson', zipcode='62701')
    bart = TSUser.createTSUser(username='bart', email='bart@simpsons.com', password='bart', address='742 Evergreen Terrace', name='Bart Simpson', zipcode='62701')
    lisa = TSUser.createTSUser(username='lisa', email='lisa@simpsons.com', password='lisa', address='742 Evergreen Terrace', name='Lisa Simpson', zipcode='62701')

def create_tools():
    homer = TSUser.objects.filter(user__username__exact='homer')[0]
    create_tool(user=homer, name='donut', location='H', desc='stale donut', img='donut.jpg')
    create_tool(user=homer, name='duff can', location='H', desc='empty Duff can', img='duff.jpg')
    create_tool(user=homer, name='nuclear plant', location='H', desc='abandoned', img='nuke.gif')
    create_tool(user=homer, name='new pen', location='H', desc='brand new pen', img='pen.jpg')
    create_tool(user=homer, name='screwdriver', location='H', desc='screwdriver', img='screwdriver.jpg')
    create_tool(user=homer, name='sofa repair kit', location='H', desc='leather and vinyl sofa repair kit', img='sofa_repair.jpg')

    bart = TSUser.objects.filter(user__username__exact='bart')[0]
    create_tool(user=bart, name='green skateboard', location='H', desc='my favorite one', img='skateboard.jpg')
    create_tool(user=bart, name='space skateboard', location='H', desc='space surfer', img='skateboard2.jpg')
    create_tool(user=bart, name='bart skateboard', location='H', desc='old one (rusted wheels)', img='skateboard3.jpg')

    lisa = TSUser.objects.filter(user__username__exact='lisa')[0]
    create_tool(user=lisa, name='sax', location='H', desc='saxophone', img='saxophone.jpg')
    create_tool(user=lisa, name='book', location='H', desc='fascinating read!', img='book.png')

    marge = TSUser.objects.filter(user__username__exact='marge')[0]
    create_tool(user=marge, name='saucepot', location='H', desc='sauce pot for cooking', img='saucepot.jpg')
    create_tool(user=marge, name='saucepan', location='H', desc='sauce pan for cooking', img='saucepan.png')
    create_tool(user=marge, name='bandaids', location='H', desc='colored bandaids', img='bandaids.jpg')


def create_borrows():
    marge = TSUser.objects.filter(user__username__exact='marge')[0]
    donut = Tool.objects.filter(name__exact='donut')[0]
    date_from = timezone.now() - timedelta(days=2)
    date_to = timezone.now() - timedelta(days=1)
    bR = BorrowTransaction.createBT(tool=donut, borrower=marge, date_f=date_from, date_t=date_to, arr='thanks!')
    bR.bt_approve()
    bR.bt_return()
    bR.bt_done()

    lisa = TSUser.objects.filter(user__username__exact='lisa')[0]
    skateboard = Tool.objects.filter(name__exact='green skateboard')[0]
    date_from = timezone.now() - timedelta(days=13)
    date_to = timezone.now() - timedelta(days=2)
    bR = BorrowTransaction.createBT(tool=skateboard, borrower=lisa, date_f=date_from, date_t=date_to, arr='need it...')
    bR.bt_approve()
    bR.bt_return()

    bart = TSUser.objects.filter(user__username__exact='bart')[0]
    duff = Tool.objects.filter(name__exact='duff can')[0]
    date_from = timezone.now() - timedelta(days=2)
    date_to = timezone.now() + timedelta(days=3)
    bR = BorrowTransaction.createBT(tool=duff, borrower=bart, date_f=date_from, date_t=date_to, arr='for science')
    bR.bt_approve()

    date_from = timezone.now() + timedelta(days=1)
    date_to = timezone.now() + timedelta(days=2)
    bR = BorrowTransaction.createBT(tool=donut, borrower=bart, date_f=date_from, date_t=date_to, arr='for lunch test')
