from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from . import forms


# Create your views here.

def signupPage(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
		else:
			form = SignUpForm()
		return render(request, 'admin.html', {'form' :form})
		
# @login_required(login_url="/login")
def userPage(request):
	current_user = request.user
	context = {
		'current_user': current_user
	}
	return render(request, 'user.html', context)

# @login_required(login_url="/login")	
def adminPage(request):
	return render(request, 'admin.html', {'variable':''})
	
@login_required(login_url="/login")
def defaultPage(request):
	return render(request, 'admin.html', {'variable':''})