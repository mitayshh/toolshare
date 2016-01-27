from django.contrib import admin

from toolshare.models import *

@admin.register(TSUser)
class TSUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'zoneID')

@admin.register(BorrowTransaction)
class BTAdmin(admin.ModelAdmin):
    list_display = ('borrowerID', 'toolID', 'borrowDate', 'dueDate')

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'ownerID', 'shareLocation')

@admin.register(Shed)
class ShedAdmin(admin.ModelAdmin):
    list_display = ('name', 'zoneID')

# @admin.register(ShareZone)
# class SZAdmin(admin.ModelAdmin):
#     list_display = ('zipcode', ['admins'])

@admin.register(Notification)
class NotifyAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'sender', 'read', 'date', 'url')

@admin.register(ToolRating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('toolID','vote_one','vote_two','vote_three','vote_four','vote_five', 'unconfirmed_vote')

@admin.register(UserRating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('userID','vote_one','vote_two','vote_three','vote_four','vote_five')