from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from . import forms


# Create your views here.

def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.refresh_from_db()
			user.profile.usertype = form.clean_data.get('usertype')
			user.profile.userID = form.clean_data.get('userID')
			user.save()
	else:
		form = SignUpForm()
			
	context = {
		'signupForm' :form
	}
	return render(request, 'admin.html', context)
		
@login_required(login_url="/login")
def userPage(request):
	current_user = request.user
	context = {
		'current_user': current_user
	}
	return render(request, 'user.html', context)

@login_required(login_url="/login")	
def adminPage(request):
		
	return render(request, 'admin.html', {'variable':''})
	
@login_required(login_url="/login")
def defaultPage(request):
	return render(request, 'user.html', {'variable':''})