from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'input-field'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'class': 'input-field'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password', 'class': 'input-field'})
    )

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'input-field'}),
        label='Email',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'class': 'input-field'}),
        label='Password',
    )
