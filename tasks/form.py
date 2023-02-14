from django import forms
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,SetPasswordForm, PasswordChangeForm
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Description'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
class CustomUserCreationForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email'] 
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'first_name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'last_name'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'email'}),
            
        }

