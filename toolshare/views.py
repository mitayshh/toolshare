"""
    File:       mysite/toolshare/views.py
    Language:   Python 2.7 with Django Web Framework

    Author:     Larwan Berke      <lwb2627@rit.edu>
    Author:     Mitayshh Dhaggai  <mxd3549@rit.edu>
    Author:     Arun Gopinathan   <ag7941@rit.edu>
    Author:     Noella Kolash     <nak8595@rit.edu>
    Author:     Andrew Marone     <agm1392@rit.edu>

    File Description: All of the different views or types of pages we need for this toolshare project.
    """

from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotFound
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth import *
from PIL import Image

# https://docs.djangoproject.com/en/1.8/topics/auth/default/#the-login-required-decorator
# don't forget to set LOGIN_URL in settings.py
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import *

# load our data classes here
from django.contrib.auth.models import User
from toolshare.models import *
from toolshare.forms import *
from django.db.models import Q
from mysite import settings

# the front page :)
def index(request, msg=False, err=False):
    args = {}
    if msg:
        args['message'] = msg
    if err:
        args['error'] = err

    if not request.user.is_authenticated():
        return render(request, 'toolshare/index.html', args)
    else:
        # admin users go to separate section of the code!
        if request.user.is_superuser:
            return HttpResponseRedirect('/admin')
        else:
            return HttpResponseRedirect('/toolshare/zone')

def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/toolshare/zone')
    else:
        if request.method=='POST':
            try:
                form = RegisterForm(request.POST)
                if form.is_valid():
                    if not form.isPasswordCorrect():
                        return render(request, 'toolshare/register.html', {
                        'error': "Password and Retyped Password do not match!",
                        'form': form,
                    })

                    # create the user object!
                    tsu = TSUser.createTSUser(username=form.get_username(), email=form.get_email(), password=form.get_password(), address=form.get_address(), name=form.get_name(), zipcode=form.get_zipcode())

                    return index(request, msg="Registered!")
                else:
                    return render(request, 'toolshare/register.html', {
                        'error': "Unable to register: invalid form data!",
                        'form': form,
                    })
            except Exception as e:
                return index(request, err='Unable to register: %s' % e)
        else:
            return render(request, 'toolshare/register.html', {
                    'form': RegisterForm(),
                })

def login(request):
    if request.user.is_authenticated():
        # TODO utilize the "next" URL if provided?
        return HttpResponseRedirect('/toolshare/zone')
    else:
        if request.method=='POST':
            # attempt to auth
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        django_login(request, user)
                        return HttpResponseRedirect('/toolshare/zone')
                    else:
                        return index(request, err="Unable to login: account disabled!")
                else:
                    return index(request, err="Unable to login: unknown user or invalid password!")
            else:
                return index(request, err="Unable to login: invalid form data!")
        else:
            return index(request, err="Unable to login: no credentials provided!")

def logout(request):
    django_logout(request)
    return index(request, msg="Logged out!")

@login_required
def profile_view(request, msg=False, err=False):
    args = {'stats': request.user.tsuser.statistics()}
    if msg:
        args['message'] = msg
    if err:
        args['error'] = err

    return render(request, 'toolshare/profile/index.html', args)

@login_required
def user_profile(request, userID, originPage=False):
    try:
        aTSUser = TSUser.objects.get(pk=userID)

        if aTSUser is None:
            raise Exception('No such user exists!')

        if aTSUser == request.user.tsuser:
            raise Exception('Borrower & Owner cannot be the same!')

        args = {'tsuser': aTSUser}

        if originPage == 'share':
            args['back_url'] = '/toolshare/share'
            args['back_desc'] = 'Back to Share Requests'
        elif originPage == 'borrow':
            args['back_url'] = '/toolshare/borrow'
            args['back_desc'] = 'Back to Borrow Requests'
        elif originPage == 'zone':
            args['back_url'] = '/toolshare/zone/users'
            args['back_desc'] = 'Back to Users'

        userRating = UserRating.objects.get(userID=userID)

        if userRating is None:
            raise Exception('No Rating available for borrower!')
        else:
            args['userRating'] = userRating

            totalUserRating = userRating.totalUserRatings()

            vote_onePercentage = 0
            vote_twoPercentage = 0
            vote_threePercentage = 0
            vote_fourPercentage = 0
            vote_fivePercentage = 0

            if totalUserRating > 0:
                vote_onePercentage = userRating.vote_one * 100 / totalUserRating
                vote_twoPercentage = userRating.vote_two * 100 / totalUserRating
                vote_threePercentage = userRating.vote_three * 100 / totalUserRating
                vote_fourPercentage = userRating.vote_four * 100 / totalUserRating
                vote_fivePercentage = userRating.vote_five * 100 / totalUserRating
                args['vote_one'] = vote_onePercentage
                args['vote_two'] = vote_twoPercentage
                args['vote_three'] = vote_threePercentage
                args['vote_four'] = vote_fourPercentage
                args['vote_five'] = vote_fivePercentage

        return render(request, 'toolshare/profile/profile.html', args)
    except Exception as e:
        return tools_index(request, err='Unable to display User Profile: %s' % e)

def shareUser_profile(request, userID):
    try:
        return user_profile(request, userID, originPage='share')
    except Exception as e:
        return tools_index(request, err='Unable to display User Profile: %s' % e)

def borrowUser_profile(request, userID):
    try:
        return user_profile(request, userID, originPage='borrow')
    except Exception as e:
        return tools_index(request, err='Unable to display User Profile: %s' % e)

def zoneUser_profile(request, userID):
    try:
        return user_profile(request, userID, originPage='zone')
    except Exception as e:
        return tools_index(request, err='Unable to display User Profile: %s' % e)

@login_required
def profile_edit(request):
    if request.method=='POST':
        try:
            form = RegistrationDetailsForm(request.POST)
            if form.is_valid():
                # update the Django user object
                if request.user.email != form.cleaned_data['email']:
                    request.user.email = form.get_email()
                    request.user.save()

                # update the TSUser object
                request.user.tsuser.name = form.get_name()
                request.user.tsuser.address = form.get_address()

                newZipCode = form.get_zipcode()

                # Check if current user is admin
                # if NORMAL USER, check if he has any transactions that is not done
                    # if he has borrowed any tool & not confirmed return yet
                    # if he is owner of any tool & not confirmed a return yet
                # If ADMIN, we need to assign ADMIN ROLE to some other user (possible integration with good RATES)

                # Check if the user did change the ZIPCODE
                if newZipCode != request.user.tsuser.zoneID:
                    aTSUser = request.user.tsuser

                    if BorrowTransaction.isTransactionPending(aTSUser):

                        return render(request, 'toolshare/profile/edit.html', {
                            'error': "You cannot move out of this Sharezone as you have a pending transaction",
                            'form': form
                        })

                    else:
                        try:
                            aSharezone = ShareZone.objects.get(zipcode__exact = newZipCode)
                        except ShareZone.DoesNotExist:
                            aSharezone = None

                        # Check for sharezone and create if necessary
                        if aSharezone is None:
                            newShareZone = ShareZone.objects.create(zipcode = newZipCode)
                            newShareZone.admins.add(request.user.tsuser)
                            newShareZone.save()
                            aSharezone = newShareZone

                        # Check if user is Admin
                        if aTSUser.zoneID.adminID == aTSUser:

                            currentShareZone = aTSUser.zoneID

                            # Get all other users in the sharezone
                            # If user is the only ONE in the Sharezone, DELETE the Sharezone, once he is shifted to new Sharezone
                            totalUsersInSharezone = TSUser.objects.filter(zoneID = request.user.tsuser.zoneID)

                            if len(totalUsersInSharezone) == 1:
                                currentShareZone.delete()
                            else:
                                # Assign any one of them as ADMIN
                                currentShareZone.assignNewAdmin(aTSUser, totalUsersInSharezone)

                        request.user.tsuser.zoneID = aSharezone

                request.user.tsuser.save()

                return profile_view(request, msg="Your profile is Updated.")
            else:
                return render(request, 'toolshare/profile/edit.html', {
                    'error': "Unable to edit profile: invalid form data!",
                    'form': form
                })
        except Exception as e:
            return profile_view(request, err='Unable to edit profile: %s' % e)
    else:
        TSUserFormValues = {'username':request.user.username,
                            'email': request.user.email,
                            'name': request.user.tsuser.name,
                            'address': request.user.tsuser.address,
                            'zipcode': request.user.tsuser.zoneID}

        form = RegistrationDetailsForm(initial=TSUserFormValues)

        return render(request, 'toolshare/profile/edit.html', {
            'form': form,
        })

@login_required
def password_change(request):
    # return HttpResponseRedirect('/toolshare')

    if request.method=='POST':
        try:
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                if not request.user.tsuser.isValidCurrentPassword(form.get_currentPassword()):
                    return render(request, 'toolshare/profile/password_change.html', {
                    'error': "Current Password is incorrect!",
                    'form': form,
                    })
                else:
                    if not form.isNewPasswordCorrect():
                        return render(request, 'toolshare/profile/password_change.html', {
                        'error': "New Password and Retyped Password do not match!",
                        'form': form,
                        })
                    else:
                        if not request.user.tsuser.areNewAndOldPasswordSame(form.get_newPassword()):
                            return render(request, 'toolshare/profile/password_change.html', {
                            'error': "New Password and Current Password should NOT be the same!",
                            'form': form,
                            })
                        else:
                            # currentUser = request.user.tsuser.userForPassword(form.get_newPassword())
                            currentUser = request.user
                            currentUser.set_password(form.get_newPassword())
                            currentUser.save()
                            # update_session_auth_hash(request, currentUser)

                            django_logout(request)
                            return index(request, msg="Password changed successfully. Login with your new credentials!")
            else:
                return render(request, 'toolshare/profile/password_change.html', {
                    'error': "Unable to register: invalid form data!",
                    'form': form,
                })
        except Exception as e:
            return index(request, err='Unable to register: %s' % e)
    else:
        return render(request, 'toolshare/profile/password_change.html', {
                'form': ChangePasswordForm(),
            })

    # return render(request, 'toolshare/profile/index.html', {
    #     'message': 'Password Changed!',
    #     'stats': request.user.tsuser.statistics()
    # })

@login_required
def password_change_done(request):
    return render(request, 'toolshare/profile/index.html', {
        'message': 'Password Changed!',
        'stats': request.user.tsuser.statistics()
    })

@login_required
def tools_index(request, msg=False, err=False, form=False):
    args = {'toolsList': request.user.tsuser.get_my_tools()}
    if msg:
        args['message'] = msg
    if err:
        args['error'] = err
    if form:
        args['form'] = form
    else:
        args['form'] = ToolRegistration()

    return render(request, 'toolshare/tools/index.html', args)

@login_required
def tools_add(request):
    try:
        if request.method=='POST':
            form = ToolRegistration(request.POST, request.FILES)
            if form.is_valid():
                # double-check that we actually have a shed!
                if form.cleaned_data['shareLocation'] == 'S':
                    shed = Shed.objects.filter(zoneID = request.user.tsuser.zoneID)
                    if not shed:
                        return tools_index(request, err="Unable to add Tool: Community Shed not setup yet!", form=form)

                # create the new Tool object!
                aTool = Tool.createTool(owner = request.user.tsuser,
                                name = form.cleaned_data['name'],
                                loc = form.cleaned_data['shareLocation'],
                                desc = form.cleaned_data['toolDescription'],
                                img = form.cleaned_data['toolImage']
                                )

                return tools_index(request, msg="Added new Tool!")
            else:
                return tools_index(request, err="Unable to add Tool: invalid form data!", form=form)
        else:
            return tools_index(request)
    except Exception as e:
        return tools_index(request, err='Unable to add Tool: %s' % e)

@login_required
def tools_del(request, toolID):
    try:
        aTool = Tool.objects.get(pk=toolID)

        # does the user actually own this tool?
        if aTool.ownerID.id != request.user.tsuser.id:
            raise Exception('tool not yours')

        # TODO cleanup anything else? maybe wrap up bR linked to this tool?
        aTool.delete()

        return tools_index(request, msg=aTool.name + " successfully deleted from the system!")
    except Exception as e:
        return tools_index(request, err='Unable to delete Tool: %s' % e)

@login_required
def tools_edit(request, toolID):
    try:
        aTool = Tool.objects.get(pk=toolID)

        # does the user actually own this tool?
        if aTool.ownerID.id != request.user.tsuser.id:
            raise Exception('tool not yours')
        else:
            if request.method=='POST':
                form = ToolRegistration(request.POST, request.FILES, instance=aTool)
                if form.is_valid():
                    # double-check that we actually have a shed!
                    if form.cleaned_data['shareLocation'] == 'S':
                        shed = Shed.objects.filter(zoneID = request.user.tsuser.zoneID)
                        if not shed:
                            return render(request, 'toolshare/tools/edit.html', {
                                'error': "Unable to edit Tool: Community Shed not setup yet!",
                                'tool': aTool,
                                'form': form,
                            })

                    # copy the data from the form to the instance ( we don't use normal form ways because of the img arg )
                    aTool.name = form.cleaned_data['name']
                    aTool.toolDescription = form.cleaned_data['toolDescription']
                    aTool.shareLocation = form.cleaned_data['shareLocation']
                    aTool.blackout_start = form.cleaned_data['blackout_start']
                    aTool.blackout_end = form.cleaned_data['blackout_end']

                    # sanity check blackout
                    if (aTool.blackout_start is None and aTool.blackout_end is not None) or (aTool.blackout_start is not None and aTool.blackout_end is None):
                        raise Exception('Blackout must be a valid date range')

                    if aTool.toolImage != form.cleaned_data['toolImage']:
                         img = form.cleaned_data['toolImage']
                         if img is None:
                             img = 'static/images/default/DefaultToolImage.jpg'

                         aTool.toolImage = img


                    aTool.save()

                    return tools_index(request, msg=aTool.name + " details have been updated!")
                else:
                    return render(request, 'toolshare/tools/edit.html', {
                        'error': "Unable to edit Tool: invalid form data!",
                        'tool': aTool,
                        'form': form,
                    })
            else:
                return render(request, 'toolshare/tools/edit.html', {
                        'tool': aTool,
                        'form': ToolRegistration(instance=aTool),
                    })
    except Exception as e:
        return tools_index(request, err='Unable to edit Tool: %s' % e)

@login_required
def tools_activate(request, toolID):
    try:
        aTool = Tool.objects.get(pk=toolID)

        # does the user actually own this tool?
        if aTool.ownerID.id != request.user.tsuser.id:
            raise Exception('tool not yours')
        else:
            aTool.isActive = True
            aTool.save()
            return tools_index(request, msg=aTool.name + " is Activated!")
    except Exception as e:
        return tools_index(request, err='Unable to activate Tool: %s' % e)

@login_required
def tools_deactivate(request, toolID):
    try:
        aTool = Tool.objects.get(pk=toolID)

        # does the user actually own this tool?
        if aTool.ownerID != request.user.tsuser:
            raise Exception('tool not yours')
        else:
            aTool.isActive = False
            aTool.save()
            return tools_index(request, msg=aTool.name + " is Deactivated!")
    except Exception as e:
        return tools_index(request, err='Unable to deactivate Tool: %s' % e)

@login_required
def borrow_index(request, msg=False, err=False, returnedToolID=False):
    args = {'borrows': request.user.tsuser.get_borrows()}

    if msg:
        args['message'] = msg
    if err:
        args['error'] = err

    return render(request, 'toolshare/borrow/index.html', args)

@login_required
def borrow_request(request, toolID):
    # validate the tool
    try:
        tool = Tool.objects.get(pk=toolID)
        if tool.ownerID == request.user.tsuser:
            raise Exception('invalid tool')

        if request.method=='POST':
            form = BorrowTransactionEditor(request.POST)
            if form.is_valid():
                # create the new Borrow object!
                t = BorrowTransaction.createBT( borrower = request.user.tsuser,
                                                tool = tool,
                                                date_f = form.cleaned_data['borrowDate'],
                                                date_t = form.cleaned_data['dueDate'],
                                                arr = form.cleaned_data['borrower_arrangements'],
                )

                return borrow_index(request, msg='Borrow request for "%s" added!' % tool.name)
            else:
                return render(request, 'toolshare/borrow/request.html', {
                    'error': "Unable to request to borrow: invalid form data!",
                    'form': form,
                    'tool': tool,
                    'date_f': form.cleaned_data['borrowDate'],
                    'date_t': form.cleaned_data['dueDate']
                })
        else:
            args = {
                'form': BorrowTransactionEditor(),
                'tool': tool,
            }
            if tool.blackout_start is not None:
                args['bl_f'] = tool.blackout_start
                args['bl_t'] = tool.blackout_end

            return render(request, 'toolshare/borrow/request.html', args)
    except Exception as e:
        return zone_index(request, err='Unable to request to borrow: %s' % e)

@login_required
def borrow_status(request, shareID):
    try:
        t = BorrowTransaction.objects.get(pk=shareID)
        if t.borrowerID != request.user.tsuser:
            raise Exception('invalid user')

        return render(request, 'toolshare/borrow/status.html', {
            'bR': t,
        })
    except Exception as e:
        return borrow_index(request, err='Unable to view borrow request: %s' % e)

@login_required
def borrow_abort(request, shareID):
    try:
        t = BorrowTransaction.objects.get(pk=shareID)
        if t.borrowerID != request.user.tsuser:
            raise Exception('invalid user')

        t.bt_abort()

        return borrow_index(request, msg='Aborted borrow request for "%s"!' % t.toolID.name)
    except Exception as e:
        return borrow_index(request, err='Unable to abort borrow request: %s' % e)

@login_required
def borrow_return(request, shareID):
    try:
        args = {'borrows': request.user.tsuser.get_borrows()}
        t = BorrowTransaction.objects.get(pk=shareID)
        if t.borrowerID != request.user.tsuser:
            raise Exception('invalid user')

        t.bt_return()

        # ask borrower to rate the tool
        return render(request, 'toolshare/rating/tool_rating.html', {
            'message': 'Returning "%s"!' % t.toolID.name,
            'returnedToolID': t.toolID.id,
        })
    except Exception as e:
        return borrow_index(request, err='Unable to return tool: %s' % e)

@login_required
def borrow_edit(request, shareID):
    try:
        t = BorrowTransaction.objects.get(pk=shareID)
        if t.borrowerID != request.user.tsuser:
            raise Exception('invalid user')
        if t.isDone:
            raise Exception('already done')

        if request.method=='POST':
            form = BorrowTransactionEditor(request.POST, instance=t)
            if form.is_valid():
                # tried to change date after approval?
                if t.isApproved is not None:
                    if (t.borrowDate != form.cleaned_data['borrowDate']) or (t.dueDate != form.cleaned_data['dueDate']):
                        raise Exception('Cannot change dates after owner decision!')

                form.save()

                return borrow_index(request, msg="Borrow request edited!")
            else:
                return render(request, 'toolshare/borrow/edit.html', {
                    'error': "Unable to edit borrow: invalid form data!",
                    'form': form,
                    'bR': t,
                })
        else:
            return render(request, 'toolshare/borrow/edit.html', {
                'form': BorrowTransactionEditor(instance=t),
                'bR': t,
            })
    except Exception as e:
        return borrow_index(request, err='Unable to edit borrow: %s' % e)

@login_required
def rate_tool(request, returnedToolID, rating):
    if len(rating) > 0:
        aTool = Tool.objects.get(pk=returnedToolID)

        try:
            if aTool is None:
                raise Exception('No such tool exists!')

            if not aTool.isActive:
                raise Exception('Cannot rate a deactivated Tool!')

            if aTool.borrowerID.id != request.user.tsuser.id:
                raise Exception('Cannot rate tool you have not borrowed!')

            if aTool.ownerID.id == request.user.tsuser.id:
                raise Exception('Owner cannot rate his own tool')

            toolRating = ToolRating.objects.get(toolID=returnedToolID)

            if toolRating is None:
                raise Exception('No Rating available for selected tool!')
            else:
                if int(rating):
                    toolRating.unconfirmed_vote = int(rating)
                    toolRating.save()
                else:
                    raise Exception('Rating is not an integer!')


                return borrow_index(request, msg=aTool.name + " was successfully Rated!")

        except Exception as e:
            return borrow_index(request, err='Unable to rate Tool: %s' % e)

    else:
        return borrow_index(request, err="Tool was not Rated!")

@login_required
def share_index(request, msg=False, err=False):
    args = {'shares': request.user.tsuser.get_shares()}

    if msg:
        args['message'] = msg
    if err:
        args['error'] = err

    return render(request, 'toolshare/share/index.html', args)

@login_required
def share_status(request, shareID):
    try:
        t = BorrowTransaction.objects.get(pk=shareID)
        if t.toolID.ownerID != request.user.tsuser:
            raise Exception('invalid user')

        return render(request, 'toolshare/share/status.html', {
            'bR': t,
        })
    except Exception as e:
        return share_index(request, err='Unable to view share request: %s' % e)

@login_required
def share_approve(request, shareID):
    try:
        t = BorrowTransaction.objects.get(pk=shareID)
        if t.toolID.ownerID != request.user.tsuser:
            raise Exception('invalid user')

        t.bt_approve()

        return share_index(request, msg='Approved sharing request for "%s"!' % t.toolID.name)
    except Exception as e:
        return share_index(request, err='Unable to approve share request: %s' % e)

@login_required
def share_deny(request, shareID, comment):
    try:
        t = BorrowTransaction.objects.get(pk=shareID)
        if t.toolID.ownerID != request.user.tsuser:
            raise Exception('invalid user')

        if comment == '':
            raise Exception('Comments required')

        t.bt_deny(ownerComment=comment)

        return share_index(request, msg='Denied sharing request for "%s"!' % t.toolID.name)
    except Exception as e:
        return share_index(request, err='Unable to deny share request: %s' % e)

@login_required
def share_done(request, shareID):
    try:
        t = BorrowTransaction.objects.get(pk=shareID)
        if t.toolID.ownerID != request.user.tsuser:
            raise Exception('invalid user')

        t.bt_done()

        # ask tool owner to rate the borrower
        return render(request, 'toolshare/rating/user_rating.html', {
            'message': 'Marking share request for "%s" as done!' % t.toolID.name,
            'borrowerID': t.borrowerID.id,
        })
    except Exception as e:
        return share_index(request, err='Unable to mark share as done: %s' % e)

@login_required
def share_notDone(request, shareID):
    try:
        t = BorrowTransaction.objects.get(pk=shareID)
        if t.toolID.ownerID != request.user.tsuser:
            raise Exception('invalid user')

        t.bt_undone()

        return share_index(request, msg="Marking Tool as not returned!")
    except Exception as e:
        return share_index(request, err='Unable to revert share: %s' % e)

@login_required
def share_edit(request, shareID):
    try:
        t = BorrowTransaction.objects.get(pk=shareID)
        if t.toolID.ownerID != request.user.tsuser:
            raise Exception('invalid user')
        if t.isDone:
            raise Exception('already done')

        if request.method=='POST':
            form = BorrowTransactionOwnerEditor(request.POST, instance=t)
            if form.is_valid():
                form.save()

                return share_index(request, msg="Share request edited!")
            else:
                return render(request, 'toolshare/share/edit.html', {
                    'error': "Unable to edit share: invalid form data!",
                    'form': form,
                    'bR': t,
                })
        else:
            return render(request, 'toolshare/share/edit.html', {
                'form': BorrowTransactionOwnerEditor(instance=t),
                'bR': t,
            })
    except Exception as e:
        return share_index(request, err='Unable to edit share: %s' % e)

@login_required
def rate_user(request, borrowerID, rating):
    if len(rating) > 0:
        aUser = TSUser.objects.get(pk=borrowerID)

        try:
            if aUser is None:
                raise Exception('No such user exists!')

            if not aUser.user.is_active:
                raise Exception('Cannot rate a deactivated User!')

            if aUser.id == request.user.tsuser.id:
                raise Exception('Owner cannot rate yourself')

            userRating = UserRating.objects.get(userID=borrowerID)

            if userRating is None:
                raise Exception('No Rating available for selected user!')
            else:
                if int(rating):
                    userRating.rateUser(int(rating))
                else:
                    raise Exception('Rating is not an integer!')

                return share_index(request, msg=aUser.name + " was successfully Rated!")

        except Exception as e:
            return share_index(request, err='Unable to rate User: %s' % e)

    else:
        return share_index(request, err="User was not Rated!")

@login_required
def zone_users(request, msg=False, err=False, customUsersList=False, searchText=False, searchCategory=False):

    args = {}

    if request.user.tsuser.isUserAnAdmin():
        if searchText:
            args = {'usersList': customUsersList}
            args['didSearch']= True
            args['searchText'] = searchText
            args['searchCategory'] = searchCategory
        else:
            args = {'usersList': request.user.tsuser.get_zone_users()}
            args['searchCategory'] = 'Search Category'

        if msg:
            args['message'] = msg
        if err:
            args['error'] = err

    return render(request, 'toolshare/zone/users.html', args)

@login_required
def zone_users_disable(request, userID):

    try:
        aTSUser = TSUser.objects.get(pk=userID)

        if not request.user.tsuser.isUserAnAdmin():
            raise Exception('Only Admins are allowed to disable a User!')

        if aTSUser is None:
            raise Exception('No such user exists!')
        else:
            aTSUser.user.is_active = not aTSUser.user.is_active
            aTSUser.user.save()

            if aTSUser.user.is_active:
                return zone_users(request, aTSUser.name + " is now enabled!")
            else:
                return zone_users(request, aTSUser.name + " is now disabled!")
    except Exception as e:
        return zone_index(request, err='Unable to view tool: %s' % e)


@login_required
def zone_addAdmin(request, userID):

    try:
        aTSUser = TSUser.objects.get(pk=userID)

        if not request.user.tsuser.isUserAnAdmin():
            raise Exception('Only Admins are allowed to disable a User!')

        if aTSUser is None:
            raise Exception('No such user exists!')
        else:

            if not aTSUser.user.is_active:
                raise Exception('Cannot provide Admin rights to disabled users!')

            # Check if user is already an ADMIN!
            if aTSUser.isUserAnAdmin():
                raise Exception('"%s" is already an Admin!' % aTSUser.name)
            else:
                userSharezone = request.user.tsuser.zoneID
                userSharezone.admins.add(aTSUser)
                userSharezone.save()
                return zone_users(request, aTSUser.name + " is now an Admin!")
    except Exception as e:
        return zone_index(request, err='Unable to provide Admin rights: %s' % e)

@login_required
def zone_index(request, msg=False, err=False, customToolsList=False, searchText=False, searchCategory=False):

    if searchText:
        paginator = Paginator(customToolsList, 9)
        page = request.GET.get('page')
        try:
            toolsList = paginator.page(page)
        except PageNotAnInteger:
            toolsList = paginator.page(1)
        except EmptyPage:
            toolsList = paginator.page(paginator.num_pages)


        args = {'toolsList': toolsList}
        args['didSearch']= True
        args['searchText'] = searchText
        args['searchCategory'] = searchCategory
    else:
        newtoolsList = request.user.tsuser.get_zone_tools()
        paginator = Paginator(newtoolsList, 9)
        page = request.GET.get('page')
        try:
            toolsList = paginator.page(page)
        except PageNotAnInteger:
            toolsList = paginator.page(1)
        except EmptyPage:
            toolsList = paginator.page(paginator.num_pages)
        args = {'toolsList': toolsList}
        args['searchCategory'] = 'Search Category'

    if msg:
        args['message'] = msg
    if err:
        args['error'] = err

    return render(request, 'toolshare/zone/index.html', args)

@login_required
def tools_search(request, toolSearchTerm):
    newtoolsList = request.user.tsuser.get_zone_tools().filter(Q(name__icontains=toolSearchTerm) | Q(ownerID__name__icontains=toolSearchTerm) | Q(toolDescription__icontains=toolSearchTerm))

    return zone_index(request, customToolsList=newtoolsList, searchText=toolSearchTerm, searchCategory='All')

@login_required
def tools_nameSearch(request, toolSearchTerm):
    newtoolsList = request.user.tsuser.get_zone_tools().filter(name__icontains=toolSearchTerm)

    return zone_index(request, customToolsList=newtoolsList, searchText=toolSearchTerm, searchCategory='Tool Name')

@login_required
def tools_ownerSearch(request, toolSearchTerm):
    newtoolsList = request.user.tsuser.get_zone_tools().filter(ownerID__name__icontains=toolSearchTerm)

    return zone_index(request, customToolsList=newtoolsList, searchText=toolSearchTerm, searchCategory='Tool Owner')

@login_required
def tools_descriptionSearch(request, toolSearchTerm):
    newtoolsList = request.user.tsuser.get_zone_tools().filter(toolDescription__icontains=toolSearchTerm)

    return zone_index(request, customToolsList=newtoolsList, searchText=toolSearchTerm, searchCategory='Tool Description')


@login_required
def tool_info(request, toolID, originPage=False):
    try:
        tool = Tool.objects.get(pk=toolID)

        # is it the owner's tool?
        # if tool.ownerID.id == request.user.tsuser.id:
        #     return HttpResponseRedirect('/toolshare/tools/edit/' + toolID)
        if tool.ownerID.zoneID != request.user.tsuser.zoneID:
            raise Exception('invalid zone')
        else:

            toolRating = ToolRating.objects.get(toolID=toolID)

            if originPage == 'wishlist':
                back_url = '/toolshare/wishlist'
                back_desc = 'Back to Wishlist'
            elif originPage == 'zone':
                back_url = '/toolshare/zone'
                back_desc = 'Back to Sharezone'

            if toolRating is None:
                raise Exception('Unable to get rating object!')
            else:
                totalToolRating = toolRating.totalToolRatings()

                vote_onePercentage = 0
                vote_twoPercentage = 0
                vote_threePercentage = 0
                vote_fourPercentage = 0
                vote_fivePercentage = 0

                if totalToolRating > 0:
                    vote_onePercentage = toolRating.vote_one * 100 / totalToolRating
                    vote_twoPercentage = toolRating.vote_two * 100 / totalToolRating
                    vote_threePercentage = toolRating.vote_three * 100 / totalToolRating
                    vote_fourPercentage = toolRating.vote_four * 100 / totalToolRating
                    vote_fivePercentage = toolRating.vote_five * 100 / totalToolRating
                return render(request, 'toolshare/zone/tool.html', {
                    'tool': tool,
                    'toolRating':toolRating,
                    'vote_one':vote_onePercentage,
                    'vote_two':vote_twoPercentage,
                    'vote_three':vote_threePercentage,
                    'vote_four':vote_fourPercentage,
                    'vote_five':vote_fivePercentage,
                    'inWishlist':tool.isToolWishlistedForUser(request.user.tsuser),
                    'back_url':back_url,
                    'back_desc':back_desc,
                })
    except Exception as e:
        return zone_index(request, err='Unable to view tool: %s' % e)

@login_required
def zone_tool(request, toolID):
    try:
        return tool_info(request, toolID, originPage='zone')
    except Exception as e:
        return tools_index(request, err='Unable to display Tool Details: %s' % e)


@login_required
def wishlist_tool(request, toolID):
    try:
        return tool_info(request, toolID, originPage='wishlist')
    except Exception as e:
        return tools_index(request, err='Unable to display Tool Details: %s' % e)

@login_required
def zone_stats(request):
    # get the stats dict
    stats = request.user.tsuser.zoneID.statistics()
    activeLenderStats = request.user.tsuser.zoneID.activeLenderStats()
    # pieDataValue = activeLenderStats['pieData']
    pieDataValue = {'pieData': activeLenderStats}

    return render(request, 'toolshare/zone/stats.html', stats)

@login_required
def shed_index(request, msg=False, err=False):
    args = {}
    if msg:
        args['message'] = msg
    if err:
        args['error'] = err

    # TODO multiple sheds?
    shed = Shed.objects.filter(zoneID = request.user.tsuser.zoneID)
    if shed:
        aTSUser = request.user.tsuser
        args['toolsList'] = Tool.objects.filter(ownerID__zoneID = aTSUser.zoneID).filter(isActive = True).filter(borrowerID = None).filter(shareLocation = 'S').exclude(ownerID = aTSUser)
        args['shed'] = shed[0]

    return render(request, 'toolshare/shed/index.html', args)

@login_required
def shed_create(zip,address):


    shed = Shed.objects.filter(zoneID = request.user.tsuser.zoneID)
    if shed:
        return shed_index(request, err="Community Shed already created in your ShareZone!")


    newShed = Shed()
    newShed.zoneID = zip
    newShed.address = address
    newShed.save()

@login_required
def shed_edit(request):
    shed = Shed.objects.filter(zoneID = request.user.tsuser.zoneID)
    if not shed:
        return shed_index(request, err="No Community Shed in your ShareZone yet!")
    else:
        shed = shed[0]

    if request.user.tsuser.zoneID.adminID != request.user.tsuser:
        return shed_index(request, err="Not ShareZone Administrator!")

    if request.method=='POST':
        form = ShedEditor(request.POST, instance=shed)
        if form.is_valid():
            form.save()

            return shed_index(request, msg="Edited the details of the Shed!")
        else:
            return render(request, 'toolshare/shed/edit.html', {
                'error': "Unable to edit the Shed: invalid form data!",
                'form': form,
            })
    else:
        return render(request, 'toolshare/shed/edit.html', {
            'form': ShedEditor(instance=shed),
        })

@login_required
def notify_index(request, msg=False, err=False):
    args = {'notifications': request.user.tsuser.getNotifications().order_by('date').reverse()}
    if msg:
        args['message'] = msg
    if err:
        args['error'] = err

    return render(request, 'toolshare/notifications/index.html', args)

@login_required
def notify_select(request,notificationID):
    try:
        notification = request.user.tsuser.getNotification(notificationID)
        if notification is None:
            raise Exception('Invalid Notification ID!')
        elif notification.recipient != request.user.tsuser:
            raise Exception('Not your own Notification!')
        else:
            notification.read = True
            notification.save()
            return HttpResponseRedirect(notification.url)
    except Exception as e:
        return notify_index(request, err='Unable to select notify: %s' % e)

@login_required
def read_all(request):
    notifs = request.user.tsuser.getNotifications()
    for notif in notifs:
        notif.read = True
        notif.save()
    return HttpResponseRedirect("../notifications")

@login_required
def add_wishlist(request, toolID):
    try:
        aTool = Tool.objects.get(pk=toolID)
        aTSUser = request.user.tsuser

        if aTool.ownerID == request.user.tsuser:
            raise Exception('Owners cannot add their tools to wishlist!')

        if aTool.isToolWishlistedForUser(aTSUser):
            raise Exception('Tool is already present in your wishlist!')
        else:
            aTool.wishListedUsers.add(aTSUser)
            return zone_index(request, msg='Tool successfully added to your wishlist!')

    except Exception as e:
        return zone_index(request, err='Unable to add tool to wishlist: %s' % e)

@login_required
def wishlist_index(request, msg=False, err=False):

    args = {}
    if msg:
        args['message'] = msg
    if err:
        args['error'] = err

    try:
        aTSUser = request.user.tsuser
        newtoolsList = aTSUser.tool_set.all()
        paginator = Paginator(newtoolsList, 9)
        page = request.GET.get('page')

        try:
            toolsList = paginator.page(page)
        except PageNotAnInteger:
            toolsList = paginator.page(1)
        except EmptyPage:
            toolsList = paginator.page(paginator.num_pages)

        args = {'wishlist': toolsList}

        return render(request, 'toolshare/tools/wishlist.html', args)
    except Exception as e:
        return zone_index(request, err='Unable to view wishlist: %s' % e)
