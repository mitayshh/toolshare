from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include

from . import views

urlpatterns = [
    # the basic URLs we will use for the user
    url(r'^$', views.index, name='index'),
    url(r'^home$', views.index, name='index'),
    url(r'^index\.html$', views.index, name='index'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^logout/$', views.logout, name='logout'),

    url(r'^profile$', views.profile_view, name='profile'),
    url(r'^profile/edit$', views.profile_edit, name='profile_edit'),
    url(r'^profile/password/change$', views.password_change, name='change_password'),
    url(r'^profile/password/change/done$', views.password_change_done, name='change_password_done'),

    # tool management
    url(r'^tools$', views.tools_index, name='tool'),
    url(r'^tools/add$', views.tools_add, name='tool_add'),
    url(r'^tools/delete/(?P<toolID>[0-9]+)$', views.tools_del, name='tool_del'),
    url(r'^tools/edit/(?P<toolID>[0-9]+)$', views.tools_edit, name='tool_edit'),
    url(r'^tools/activate/(?P<toolID>[0-9]+)$', views.tools_activate, name='tool_on'),
    url(r'^tools/deactivate/(?P<toolID>[0-9]+)$', views.tools_deactivate, name='tool_off'),

    # sharing - borrower perspective
    url(r'^borrow$', views.borrow_index, name='borrow'),
    url(r'^borrow/request/(?P<toolID>[0-9]+)$', views.borrow_request, name='borrow_ask'),
    url(r'^borrow/status/(?P<shareID>[0-9]+)$', views.borrow_status, name='borrow_status'),
    url(r'^borrow/abort/(?P<shareID>[0-9]+)$', views.borrow_abort, name='borrow_abort'),
    url(r'^borrow/return/(?P<shareID>[0-9]+)$', views.borrow_return, name='borrow_return'),
    url(r'^borrow/edit/(?P<shareID>[0-9]+)$', views.borrow_edit, name='borrow_edit'),

    url(r'^wishlist$', views.wishlist_index, name='wishlist_index'),
    url(r'^wishlist/tool/(?P<toolID>[0-9]+)$', views.wishlist_tool, name='wishlist_tool'),
    url(r'^wishlist/add/(?P<toolID>[0-9]+)$', views.add_wishlist, name='add_wishlist'),

    url(r'^tool/rate/(?P<returnedToolID>[0-9]+)/(?P<rating>[0-9]*)$', views.rate_tool, name='rate_tool'),
    url(r'^user/rate/(?P<borrowerID>[0-9]+)/(?P<rating>[0-9]*)$', views.rate_user, name='rate_user'),

    # sharing - owner perspective
    url(r'^share$', views.share_index, name='share'),
    url(r'^share/status/(?P<shareID>[0-9]+)$', views.share_status, name='share_status'),
    url(r'^share/approve/(?P<shareID>[0-9]+)$', views.share_approve, name='share_approve'),
    url(r'^share/deny/(?P<shareID>[0-9]+)/(?P<comment>.*)$', views.share_deny, name='share_deny'),
    url(r'^share/done/(?P<shareID>[0-9]+)$', views.share_done, name='share_done'),
    url(r'^share/notDone/(?P<shareID>[0-9]+)$', views.share_notDone, name='share_notDone'),
    url(r'^share/edit/(?P<shareID>[0-9]+)$', views.share_edit, name='share_edit'),

    url(r'^share/user/profile/(?P<userID>[0-9]+)$', views.shareUser_profile, name='shareUser_profile'),
    url(r'^borrow/user/profile/(?P<userID>[0-9]+)$', views.borrowUser_profile, name='borrowUser_profile'),
    url(r'^zone/users/profile/(?P<userID>[0-9]+)$', views.zoneUser_profile, name='zoneUser_profile'),

    # shed stuff
    url(r'^shed$', views.shed_index, name='shed'),
    url(r'^shed/create$', views.shed_create, name='shed_create'),
    url(r'^shed/edit$', views.shed_edit, name='shed_edit'),

    # sharezone stuff ( no need to pass zone as ID because it's part of user profile )
    url(r'^zone$', views.zone_index, name='zone'),
    url(r'^zone/users$', views.zone_users, name='zone_users'),
    url(r'^zone/users/manage/(?P<userID>[0-9]+)$', views.zone_users_disable, name='zone_users_disable'),
    url(r'^zone/users/admin/(?P<userID>[0-9]+)$', views.zone_addAdmin, name='zone_users_disable'),
    url(r'^zone/search/all/(?P<toolSearchTerm>\w*)$', views.tools_search, name='tool_search'),
    url(r'^zone/search/name/(?P<toolSearchTerm>\w*)$', views.tools_nameSearch, name='tool_nameSearch'),
    url(r'^zone/search/owner/(?P<toolSearchTerm>\w*)$', views.tools_ownerSearch, name='tool_ownerSearch'),
    url(r'^zone/search/description/(?P<toolSearchTerm>\w*)$', views.tools_descriptionSearch, name='tool_descriptionSearch'),
    url(r'^zone/tool/(?P<toolID>[0-9]+)$', views.zone_tool, name='zone_tool'),
    url(r'^zone/statistics$', views.zone_stats, name='zone_stats'),

    url(r'^notifications$', views.notify_index, name='list_notifications'),
    url(r'^notifications/(?P<notificationID>[0-9]+)$', views.notify_select, name='select_notification'),
    url(r'^notifications/readall$', views.read_all, name='read_all_notify'),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
