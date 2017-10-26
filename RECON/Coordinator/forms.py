import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from .models import EMPLOYEE_TYPE_CHOICES, Group, Profile

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username', 'placeholder': 'Username'}))
    password = forms.CharField(label="Password", max_length=30, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password', 'placeholder': 'Password'}))


class SignUpForm(UserCreationForm):
	usertype = forms.ChoiceField(
		choices=EMPLOYEE_TYPE_CHOICES,
		label="User Type",
	)
	employeeID = forms.CharField(label="Employee ID")
	group = forms.ModelChoiceField(
		queryset = Group.objects.all(),
		empty_label = None,
	)
	
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'employeeID', 'usertype', 'group',)
	
class CreateGroupForm(forms.ModelForm):

	class Meta:
		model = Group
		fields = ('name',)