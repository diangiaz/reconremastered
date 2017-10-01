from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from . import forms
from .forms import SignUpForm

# Create your views here.

		
@login_required(login_url="/login")
def userPage(request):
	current_user = request.user
	context = {
		'current_user': current_user
	}
	return render(request, 'user.html', context)

@login_required(login_url="/login")	
def adminPage(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.refresh_from_db()
			user.profile.usertype = form.cleaned_data.get('usertype')
			user.profile.userID = form.cleaned_data.get('userID')
			user.save()
	
	signupForm = SignUpForm()
		
	context = {
	'signupForm' : signupForm
	}
	return render(request, 'admin.html', context)
	