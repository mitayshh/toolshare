{% load staticfiles %}
<!DOCTYPE html>
<html>
<head>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}">
	<script type="text/javascript" src="{% static 'js/jquery.min.js' %}"></script>
	<script type="text/javascript" src="{% static 'js/bootstrap.min.js' %}"></script>
      <link rel="stylesheet" href="{% static 'css/daterangepicker.css' %}" />
      <script type="text/javascript" src="{% static 'js/moment.min.js' %}"></script>
      <script type="text/javascript" src="{% static 'js/daterangepicker.js' %}"></script>
      <script type="text/javascript" src="{% static 'js/Chart.min.js' %}"></script>
</head>
<body>

<nav class="navbar navbar-default">
  <div class="container-fluid">
    <div class="navbar-header">
	  <ul class="nav navbar-nav">
			<li {% if active_tab = 'sharezone' %} class="active"{% endif %}><a class="navbar-brand" href="/toolshare/"><span class="glyphicon glyphicon-wrench"></span> ToolShare</a></li>
	        <li {% if active_tab = 'tools' %}     class="active"{% endif %}><a href="/toolshare/tools">My Tools</a></li>
	        <li {% if active_tab = 'share' %}     class="active"{% endif %}><a href="/toolshare/share">Share Requests {% if request.user.tsuser.get_pending_share > 0 %}<span class="badge">{{ request.user.tsuser.get_pending_share }}</span>{% endif %} </a></li>
	        <li {% if active_tab = 'borrow' %}    class="active"{% endif %}><a href="/toolshare/borrow">My Borrow Requests {% if request.user.tsuser.get_pending_borrow > 0 %} <span class="badge">{{ request.user.tsuser.get_pending_borrow }}</span>{% endif %}</a></li>
	        {% if request.user.tsuser.isUserAnAdmin %}
<li {% if active_tab = 'users' %}    class="active"{% endif %}><a href="/toolshare/zone/users">Users 	</a></li>
			{% endif %}
	        <li class="{% if active_tab = 'profile' %}active{% else %}dropdown{% endif %}">
	          <a class="dropdown-toggle" data-toggle="dropdown" href="#"><span class="glyphicon glyphicon-user"></span> Hello, {{request.user.tsuser.user}}!{% if request.user.tsuser.getNotificationCount > 0 %}&nbsp;<span class="badge">{{ request.user.tsuser.getNotificationCount }}{% endif%}</span>
	          <span class="caret"></span></a>
	          <ul class="dropdown-menu">
	          	<li {% if active_tab = 'wishlist' %}class="active"{% endif %}"><a href="/toolshare/wishlist">Wishlist</a></li>
	            <li>&nbsp;</li>
	            <li {% if active_tab = 'profile' %}class="active"{% endif %}"><a href="/toolshare/profile">My Profile</a></li>
	            <li>&nbsp;</li>
	            <li><a href="/toolshare/notifications">Notifications {% if request.user.tsuser.getNotificationCount > 0 %}&nbsp;<span class="badge">{{ request.user.tsuser.getNotificationCount }}{% endif%}</span></a></li>
	            <li>&nbsp;</li>
	            <li><a href="/toolshare/logout">Logout</a></li>
	          </ul>
	        </li>
      </ul>
    </div>
  </div>
</nav>

<div class="container">

<script type="text/javascript" src="{% static 'js/notie.js' %}"></script>
{% if message or error %}
	{% if message %}
		<script language="javascript">
		$(document).ready(function() {
			notie.alert(1, '{{ message }}', 1.5 );
		});
		</script>
	{% endif %}
	{% if error %}
		<script language="javascript">
		$(document).ready(function() {
			notie.alert(3, '{{ error }}', 2 );
		});
		</script>
	{% endif %}
{% endif %}
