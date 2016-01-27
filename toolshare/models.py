"""
    File:       mysite/toolshare/models.py
    Language:   Python 2.7 with Django Web Framework

    Author:     Larwan Berke      <lwb2627@rit.edu>
    Author:     Mitayshh Dhaggai  <mxd3549@rit.edu>
    Author:     Arun Gopinathan   <ag7941@rit.edu>
    Author:     Noella Kolash     <nak8595@rit.edu>
    Author:     Andrew Marone     <agm1392@rit.edu>

    File Description: The models we need for this toolshare project.
    """
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth import authenticate

from datetime import timedelta
from django.utils import timezone
from django.db.models import Q

# Create your models here.

class ShareZone(models.Model):
    zipcode = models.IntegerField(primary_key=True)
    shedID = models.ForeignKey('toolshare.Shed', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Shed')
    admins = models.ManyToManyField('toolshare.TSUser', blank=True, verbose_name='Administrator')

    @classmethod
    def createSZ(cls, zipcode):
        sz = ShareZone.objects.create(zipcode=zipcode)
        sz.save()
        return sz

    class Meta:
        verbose_name = 'ShareZone'

    def assignNewAdmin(self, aTSUser, totalUsersInSharezone):
        newAdmin = aTSUser

        for aUser in totalUsersInSharezone:
            # TODO: Can change this based on Ratings
            if aUser != aTSUser:
                self.adminID = aUser
                self.save()
                newAdmin = aUser
                break
        return newAdmin


    def activeLenderStats(self):
        max_entries = 5
        alStats = []
        activeLenderDictionary = {}

        activeLendersCollection = BorrowTransaction.objects.filter(toolID__ownerID__zoneID = self).values('toolID__ownerID', 'toolID__ownerID__name').annotate(Count('toolID__ownerID')).order_by('-toolID__ownerID__count')[:max_entries]

        for anActiveLender in activeLendersCollection:
            anActiveLenderDict = {}
            anActiveLenderDict['value'] = anActiveLender['toolID__ownerID__count']
            anActiveLenderDict['color'] = 'F7464A'
            anActiveLenderDict['label'] = anActiveLender['toolID__ownerID__name']
            alStats.append(anActiveLenderDict)

        activeLenderDictionary['pieData'] = alStats
        activeLenderDictionary['length'] = len(activeLendersCollection)

        return  alStats
        # return activeLenderDictionary


    def statistics(self):
        max_entries = 5
        stats = {}

        stats['active_lenders'] = BorrowTransaction.objects.filter(toolID__ownerID__zoneID = self).values('toolID__ownerID', 'toolID__ownerID__name').annotate(Count('toolID__ownerID')).order_by('-toolID__ownerID__count')[:max_entries]
        stats['active_borrowers'] = BorrowTransaction.objects.filter(borrowerID__zoneID = self).values('borrowerID', 'borrowerID__name').annotate(Count('borrowerID')).order_by('-borrowerID__count')[:max_entries]
        stats['most_used_tools'] = BorrowTransaction.objects.filter(borrowerID__zoneID = self).filter(isApproved = True).values('toolID', 'toolID__name').annotate(Count('toolID')).order_by('-toolID__count')[:max_entries]

        stats['recent_borrowed_tools'] = BorrowTransaction.objects.filter(borrowerID__zoneID = self).filter(isApproved = True).values('toolID', 'toolID__name', 'borrowDate', 'toolID__ownerID__name', 'borrowerID__name').order_by('-borrowDate')[:max_entries]

        stats['tool_borrows_today'] = BorrowTransaction.objects.filter(borrowerID__zoneID = self).filter(borrowDate__range=( timezone.now() - timedelta(days=1), timezone.now() )).filter(isApproved = True).count()
        stats['tool_borrows_week'] = BorrowTransaction.objects.filter(borrowerID__zoneID = self).filter(borrowDate__range=( timezone.now() - timedelta(days=7), timezone.now() )).filter(isApproved = True).count()
        stats['tool_borrows_month'] = BorrowTransaction.objects.filter(borrowerID__zoneID = self).filter(borrowDate__range=( timezone.now() - timedelta(days=30), timezone.now() )).filter(isApproved = True).count()
        stats['tool_borrows_year'] = BorrowTransaction.objects.filter(borrowerID__zoneID = self).filter(borrowDate__range=( timezone.now() - timedelta(days=365), timezone.now() )).filter(isApproved = True).count()

        stats['user_borrows_today'] = BorrowTransaction.objects.filter(borrowerID__zoneID = self).filter(borrowDate__range=( timezone.now() - timedelta(days=1), timezone.now() )).filter(isApproved = True).values('borrowerID').annotate(Count('borrowerID')).count()
        stats['user_borrows_week'] = BorrowTransaction.objects.filter(borrowerID__zoneID = self).filter(borrowDate__range=( timezone.now() - timedelta(days=7), timezone.now() )).filter(isApproved = True).values('borrowerID').annotate(Count('borrowerID')).count()
        stats['user_borrows_month'] = BorrowTransaction.objects.filter(borrowerID__zoneID = self).filter(borrowDate__range=( timezone.now() - timedelta(days=30), timezone.now() )).filter(isApproved = True).values('borrowerID').annotate(Count('borrowerID')).count()
        stats['user_borrows_year'] = BorrowTransaction.objects.filter(borrowerID__zoneID = self).filter(borrowDate__range=( timezone.now() - timedelta(days=365), timezone.now() )).filter(isApproved = True).values('borrowerID').annotate(Count('borrowerID')).count()

        stats['user_shares_today'] = BorrowTransaction.objects.filter(borrowerID__zoneID = self).filter(borrowDate__range=( timezone.now() - timedelta(days=1), timezone.now() )).filter(isApproved = True).values('toolID__ownerID').annotate(Count('toolID__ownerID')).count()
        stats['user_shares_week'] = BorrowTransaction.objects.filter(borrowerID__zoneID = self).filter(borrowDate__range=( timezone.now() - timedelta(days=7), timezone.now() )).filter(isApproved = True).values('toolID__ownerID').annotate(Count('toolID__ownerID')).count()
        stats['user_shares_month'] = BorrowTransaction.objects.filter(borrowerID__zoneID = self).filter(borrowDate__range=( timezone.now() - timedelta(days=30), timezone.now() )).filter(isApproved = True).values('toolID__ownerID').annotate(Count('toolID__ownerID')).count()
        stats['user_shares_year'] = BorrowTransaction.objects.filter(borrowerID__zoneID = self).filter(borrowDate__range=( timezone.now() - timedelta(days=365), timezone.now() )).filter(isApproved = True).values('toolID__ownerID').annotate(Count('toolID__ownerID')).count()


        return stats

    def __str__(self):
        return str(self.zipcode)

#Extends the functionality of the models.User model
class TSUser(models.Model):
    user = models.OneToOneField(User, verbose_name='User Login')
    name = models.CharField(max_length=200, verbose_name='Full Name')
    address = models.CharField(max_length=200)
    zoneID = models.ForeignKey(ShareZone, verbose_name='ShareZone')

    @classmethod
    def createTSUser(cls, username, email, password, address, name, zipcode ):
        u = User.objects.create_user(username=username, email=email, password=password)
        u.save()

        # check for sharezone and create if necessary
        new_sz = False
        sz = ShareZone.objects.filter(zipcode__exact=zipcode)
        if not sz:
            new_sz = True
            sz = ShareZone.createSZ(zipcode=zipcode)
        else:
            sz = sz[0]

        # now, create the linked TSUser object!
        tsu = TSUser.objects.create(user=u, address=address, name=name, zoneID=sz )
        tsu.save()

        # CREATE USER RATING
        userRating = UserRating.createUserRating(user=tsu)

        if new_sz:
            sz.admins.add(tsu)
            sz.save()
            Shed.shedy(sz,address)


        return tsu

    def isValidCurrentPassword(self, currentPassword):
        return self.user.check_password(currentPassword)

    def areNewAndOldPasswordSame(self, newPassword):
        # New Password & Old Password should NOT be the SAME!
        if self.user.check_password(newPassword):
            return False
        else:
            return True

    def userForPassword(self, currentPassword):
        users = User.objects.filter(username__exact=self.user.username)

        if len(users) > 0:
            aUser = users[0]
        else:
            aUser = None

        return aUser

    def isUserAnAdmin(self):
        userSharezone = self.zoneID
        isAnAdmin = False
        for aUser in userSharezone.admins.all():
            if aUser == self:
                isAnAdmin = True
                break

        return isAnAdmin

    def notifyUser(self,sender,msg,url):
        n = Notification.objects.create(recipient = self,sender=sender,message=msg,url=url)
        n.save()

    def statistics(self):
        max_entries = 5
        stats = {}

        stats['recent_shared_tools'] = BorrowTransaction.objects.filter(toolID__ownerID = self).filter(isApproved = True).values('toolID', 'toolID__name', 'borrowDate', 'borrowerID__name').order_by('-borrowDate')[:max_entries]
        stats['recent_borrowed_tools'] = BorrowTransaction.objects.filter(borrowerID = self).filter(isApproved = True).values('toolID', 'toolID__name', 'borrowDate', 'toolID__ownerID__name').order_by('-borrowDate')[:max_entries]
        return stats

    def get_my_tools(self):
        return Tool.objects.filter(ownerID = self)

    def get_zone_tools(self):
        #Fetch tools from same shareZone & do not fetch tools owned by the current user & do not fetch inactive tools & do not fetch checked out tools
        toolsList = Tool.objects.filter(ownerID__zoneID = self.zoneID).filter(isActive = True)

        nonBorrowedToolList = []

        for aTool in toolsList:
            borrowTransactionList = BorrowTransaction.objects.filter(borrowerID = self).filter(toolID = aTool).filter(isDone = 0)
            if BorrowTransaction.objects.filter(borrowerID = self).filter(toolID = aTool).filter(isApproved = None).count() == 0:
                nonBorrowedToolList.append(aTool)

        return toolsList

    def get_zone_users(self):
        # Fetch users from same shareZone & do not fetch users currently involved in a transaction & do not fetch inactive users
        allUsersList = TSUser.objects.filter(zoneID = self.zoneID).exclude(id = self.id)
        return allUsersList

    def isUserInTransaction(self):
        inTransaction = False
        transactionsForUser = BorrowTransaction.objects.filter(isDone = 0).filter(Q(borrowerID = self.id) | Q(toolID__ownerID = self.id))
        if len(transactionsForUser) > 0:
            inTransaction = True

        return inTransaction

    def averageRating(self):
        userRating = UserRating.objects.get(userID=self.id)

        avgRating = 0

        if userRating.totalUserRatings() > 0:
            avgRating = ((userRating.vote_one * 1) + (userRating.vote_two * 2) + (userRating.vote_three * 3) + (userRating.vote_four * 4) + (userRating.vote_five * 5)) / userRating.totalUserRatings()

        return avgRating


    def get_shares(self):
        notApprovedShares = BorrowTransaction.objects.filter(toolID__ownerID = self).filter(isApproved = None).filter(isDone = False).filter(didBorrowerReturn = False)

        returnedShares = BorrowTransaction.objects.filter(toolID__ownerID = self).filter(isApproved = True).filter(isDone = False)

        shares = []

        if (len(notApprovedShares) > 0):
            shares.extend(notApprovedShares)


        if (len(returnedShares) > 0):
            shares.extend(returnedShares)

        return shares

    def get_pending_share(self):
        unapproved = BorrowTransaction.objects.filter(toolID__ownerID = self).filter(isDone = False).filter(isApproved=None).count()
        returned = BorrowTransaction.objects.filter(toolID__ownerID = self).filter(isDone = False).filter(isApproved=True).filter(didBorrowerReturn=True).count()
        return unapproved + returned

    def get_borrows(self):
        return BorrowTransaction.objects.filter(borrowerID = self).filter(isDone = False).exclude(didBorrowerReturn = True)

    def get_pending_borrow(self):
        return BorrowTransaction.objects.filter(borrowerID = self).filter(isDone = False).filter(isApproved=True).filter(didBorrowerReturn=False).count()

    def getNotification(self, notifyID):
        return Notification.objects.filter(id=notifyID)[0]

    def getNotifications(self):
        return Notification.objects.filter(recipient=self)

    def getNotificationCount(self):
        return Notification.objects.filter(recipient=self).filter(read=False).count()

    class Meta:
        verbose_name = 'ToolShare User'

    def __str__(self):
        return self.name

class Tool(models.Model):
    TOOL_LOCATIONS = (
        ('H', 'Home'),
        ('S', 'Shed')
    )
    name = models.CharField(max_length=200)
    isActive = models.BooleanField(default=True, verbose_name='Active?')
    ownerID = models.ForeignKey(TSUser, related_name='%(class)s_ownerID', verbose_name='Owner Name')
    borrowerID = models.ForeignKey(TSUser, related_name='%(class)s_borrowerID', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Current Borrower')
    shareLocation = models.CharField(max_length=1, choices=TOOL_LOCATIONS, verbose_name='Location')
    toolDescription = models.CharField(max_length=2000, verbose_name='Description')
    toolImage = models.ImageField(upload_to='static/tools', verbose_name='Image')
    wishListedUsers = models.ManyToManyField(TSUser)
    blackout_start = models.DateTimeField(default=None, blank=True, null=True, verbose_name='Blackout Start Date')
    blackout_end = models.DateTimeField(default=None, blank=True, null=True, verbose_name='Blackout End Date')

    class Meta:
        verbose_name = 'Tool'

    def __str__(self):
        return self.name

    @classmethod
    def createTool(cls, owner, name, loc, desc, img, norating=False, nonotify=False):

        if img is None:
            img = 'static/images/default/DefaultToolImage.jpg'

        aTool = Tool.objects.create( ownerID = owner,
                                     name = name,
                                     shareLocation=loc,
                                     toolDescription=desc,
                                     toolImage=img
                                     )
        aTool.save()

        # automatically create the linked rating object unless told not to
        if not norating:
            ToolRating.createToolRating(tool=aTool)

        # notify all of our users!
        if not nonotify:
            users = TSUser.objects.filter(zoneID=owner.zoneID)
            for u in users:
                # skip ourself!
                if u != owner:
                    u.notifyUser( sender = owner,
                                  msg = 'added "%s" to your ShareZone' % aTool.name,
                                  url = '/toolshare/zone/tool/%i' % aTool.id
                                  )

        return aTool


    def isToolWishlistedForUser(self, aTSUser):
        allWishListedUsers =  self.wishListedUsers.all()
        isToolInWishlist = False

        for aUser in allWishListedUsers:
            if aUser == aTSUser:
                isToolInWishlist = True
                break

        return isToolInWishlist


    def averageRating(self):
        toolRating = ToolRating.objects.get(toolID=self.id)

        avgRating = 0

        if toolRating.totalToolRatings() > 0:
            avgRating = ((toolRating.vote_one * 1) + (toolRating.vote_two * 2) + (toolRating.vote_three * 3) + (toolRating.vote_four * 4) + (toolRating.vote_five * 5)) / toolRating.totalToolRatings()

        return avgRating


class Shed(models.Model):
    name = models.CharField(max_length=200, default="Community Shed")
    zoneID = models.ForeignKey(ShareZone, verbose_name='ShareZone')
    address = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Shed'

    def __str__(self):
        return self.name + ' for ShareZone(' + str(self.zoneID.zipcode) + ')'

    @classmethod
    def shedy(cls,zone,address1):

        shed = Shed.objects.create(zoneID=zone,address=address1)
        shed.save()


class BorrowTransaction(models.Model):
    borrowerID = models.ForeignKey(TSUser, related_name='%(class)s_borrowerID', verbose_name='Borrower Name')
    toolID = models.ForeignKey(Tool, verbose_name='Tool Name')
    borrowDate = models.DateTimeField(verbose_name='Borrow Date')
    dueDate = models.DateTimeField(verbose_name='Due Date')
    isApproved = models.NullBooleanField(default=None, blank=True, null=True, verbose_name='Approved?')
    didBorrowerReturn = models.BooleanField(default=False, verbose_name='Returned?')
    isDone = models.BooleanField(default=False, verbose_name='Done?')
    borrower_arrangements = models.CharField(max_length=2000, verbose_name='Borrower Comments')
    owner_arrangements = models.CharField(default=None, blank=True, null=True, max_length=2000, verbose_name='Tool Owner Comments')

    class Meta:
        verbose_name = 'Borrow Transaction'

    def __str__(self):
        return self.borrowerID.name + ' Borrowing(' + self.toolID.name + ')'

    @classmethod
    def isTransactionPending(self, aTSUser):
        isTransactionPending = True

        nonReturnedBorrowers = BorrowTransaction.objects.filter(isDone = False).filter(borrowerID = aTSUser)
        nonReturnedOwners = BorrowTransaction.objects.filter(isDone = False).filter(toolID__ownerID = aTSUser)

        if not nonReturnedBorrowers and not nonReturnedOwners:
            isTransactionPending = False

        return isTransactionPending

    @classmethod
    def createBT(cls, borrower, tool, date_f, date_t, arr):
        # check to see if the requested dates aren't blackout'd
        if tool.blackout_start is not None:
            if tool.blackout_start.timestamp() - date_f.timestamp() > 0:
                if tool.blackout_start.timestamp() - date_t.timestamp() < 0:
                    raise Exception('Tool is Blacked Out after you wanted to check out!')

            else:
                if tool.blackout_end.timestamp() - date_f.timestamp() > 0:
                    raise Exception('Tool is Blacked Out during your check out dates!')

        t = BorrowTransaction.objects.create( borrowerID = borrower,
                                              toolID = tool,
                                              borrowDate = date_f,
                                              dueDate = date_t,
                                              borrower_arrangements = arr,
        )
        t.save()

        # notify user
        tool.ownerID.notifyUser(sender=borrower,
                                msg='is asking to borrow tool "%s"  on %s at %s' % (tool.name, date_f.strftime("%d/%m/%y"),date_f.strftime("%I:%M %p")),
                                url='/toolshare/share/status/%i' % t.id,
        )
        return t

    def bt_approve(self):
        # some simple sanity checks
        if self.isDone:
            raise Exception('done')
        if self.isApproved is not None:
            raise Exception('already decided')

        # set the tool to "checked out"
        self.toolID.borrowerID = self.borrowerID
        self.toolID.save()
        self.isApproved = True
        self.save()

        # DENYing other people's request as ONE borrower's request has been approved
        borrowTransactionList = BorrowTransaction.objects.filter(toolID = self.toolID).filter(isApproved = None)
        for t in borrowTransactionList:
            t.bt_deny( ownerComment="Another borrower was Selected" )

        # send the borrower a notify!
        self.borrowerID.notifyUser(sender=self.toolID.ownerID,
                           msg='approved your borrow request for tool "%s" on %s at %s' % (self.toolID.name, self.borrowDate.strftime("%d/%m/%y"), self.borrowDate.strftime("%I:%M %p") ),
                           url='/toolshare/borrow/status/%i' % self.id,
                           )

    def bt_deny(self, ownerComment):
        # some simple sanity checks
        if self.isDone:
            raise Exception('done')
        if self.isApproved is not None:
            raise Exception('already decided')

        # deny the borrow request
        self.isApproved = False
        self.isDone = True
        self.owner_arrangements = 'DENIED: ' + ownerComment
        self.save()

        # send notify of deny
        self.borrowerID.notifyUser(sender=self.toolID.ownerID,
                                   msg='denied your borrow request for tool "%s"' % self.toolID.name,
                                   url='/toolshare/borrow/status/%i' % self.id,
                                   )

    def bt_return(self):
        # some simple sanity checks
        if self.isApproved is None:
            raise Exception('not approved yet')
        if self.didBorrowerReturn:
            raise Exception('already returned')

        # finalize our side of the transaction
        self.didBorrowerReturn = True
        self.save()

        # send the user a notify!
        self.toolID.ownerID.notifyUser(sender=self.borrowerID,
                                       msg='returned tool "%s"' % self.toolID.name,
                                       url='/toolshare/share/status/%i' % self.id,
                                       )

    def bt_done(self):
        # some simple sanity checks
        if self.isDone:
            raise Exception('done')
        if self.isApproved is None:
            raise Exception('undecided')
        if self.isApproved is False:
            raise Exception('already denied')
        if self.didBorrowerReturn is False:
            raise Exception('borrower has not returned')

        # update the tool object!
        if self.toolID.borrowerID == self.borrowerID:
            self.toolID.borrowerID = None
            self.toolID.save()
        else:
            raise Exception('invalid tool link')

        # all done!
        self.isDone = True
        self.save()

        # The Tool Rating will be reflected only once the Owner confirms the Tool has been returned
        toolRating = ToolRating.objects.get(toolID=self.toolID)
        toolRating.confirmRating()

        # send the Wishlisted Users a Notification!
        wishListedUsers = self.toolID.wishListedUsers.all()

        for aUser in wishListedUsers:
            aUser.notifyUser(sender=self.toolID.ownerID,
                            msg='Wishlisted Tool,"%s" is now available' % self.toolID.name,
                            url='/toolshare/zone/tool/%i' % self.toolID.id,
                            )


    def bt_undone(self):
        # some simple sanity checks
        if self.isDone:
            raise Exception('already done')
        if self.isApproved is None:
            raise Exception('undecided')
        if self.isApproved is False:
            raise Exception('already denied')
        if self.didBorrowerReturn is False:
            raise Exception('borrower has not returned')

        # Reverting back to didborrowerReturn
        self.didBorrowerReturn = False
        self.save()

        # Nullify Tool Rating as Owner has not confirmed TOOL RETURN yet
        toolRating = ToolRating.objects.get(toolID=self.toolID)
        toolRating.nullifyRating()

    def bt_abort(self):
        # some simple sanity checks
        if self.isDone:
            raise Exception('already done')
        if self.isApproved is not None:
            raise Exception('already decided')

        # remove the notification from this request!
        thenotify = Notification.objects.filter(url__exact='/toolshare/share/status/%i' % self.id)
        if thenotify.count() == 1:
            if thenotify[0].read:
                raise Exception('Tool owner already read notification!')
            else:
                thenotify[0].delete()
        else:
            raise Exception('unable to locate associated notification object')

        # all done!
        self.isDone = True
        self.save()

class ToolRating(models.Model):
    toolID = models.ForeignKey(Tool, verbose_name='Tool')
    vote_one = models.IntegerField(default=0)
    vote_two = models.IntegerField(default=0)
    vote_three = models.IntegerField(default=0)
    vote_four = models.IntegerField(default=0)
    vote_five = models.IntegerField(default=0)
    unconfirmed_vote = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Rating'

    def __str__(self):
        return self.toolID.name + ' Avg(' + str(self.avgRating()) + ')'

    def confirmRating(self):
        if self.unconfirmed_vote > 0:
            if self.unconfirmed_vote == 1:
                self.vote_one += 1
            elif self.unconfirmed_vote == 2:
                self.vote_two += 1
            elif self.unconfirmed_vote == 3:
                self.vote_three += 1
            elif self.unconfirmed_vote == 4:
                self.vote_four += 1
            else:
                self.vote_five += 1

            self.unconfirmed_vote = 0
            self.save()

    def nullifyRating(self):
        if self.unconfirmed_vote > 0:
            self.unconfirmed_vote = 0
            self.save()

    @classmethod
    def createToolRating(cls, tool):
        r = ToolRating.objects.create(toolID=tool)
        r.save()
        return r

    def totalToolRatings(self):
        return (self.vote_one + self.vote_two + self.vote_three + self.vote_four + self.vote_five)


class UserRating(models.Model):
    userID = models.ForeignKey(TSUser, verbose_name='User')
    vote_one = models.IntegerField(default=0)
    vote_two = models.IntegerField(default=0)
    vote_three = models.IntegerField(default=0)
    vote_four = models.IntegerField(default=0)
    vote_five = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'UserRating'

    def __str__(self):
        return self.userID.name + ' Avg(' + str(self.avgRating()) + ')'

    def rateUser(self, rating):
        if rating == 1:
            self.vote_one += 1
        elif rating == 2:
            self.vote_two += 1
        elif rating == 3:
            self.vote_three += 1
        elif rating == 4:
            self.vote_four += 1
        elif rating == 5:
            self.vote_five += 1
        else:
            raise Exception('Unknown rating!')

        self.save()

    @classmethod
    def createUserRating(cls, user):
        userRating = UserRating.objects.create(userID=user)
        userRating.save()
        return userRating

    def totalUserRatings(self):
        return (self.vote_one + self.vote_two + self.vote_three + self.vote_four + self.vote_five)


class Notification(models.Model):
    recipient = models.ForeignKey(TSUser, related_name='%(class)s_recip')
    sender = models.ForeignKey(TSUser, related_name='%(class)s_sender')
    date = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    read = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'User Notification'

    def __str__(self):
        return self.recipient.name + ' (' + self.date.isoformat() + ')'
