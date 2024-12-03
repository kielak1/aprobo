# forms.py
from django import forms
from django.contrib.auth.models import User


class ImportForm(forms.Form):
    excel_file = forms.FileField()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "first_name", "email")

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 12 or len(password) > 128:
            raise forms.ValidationError(
                "Password must be between 12 and 128 characters."
            )
        return password

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match.")
        return password2
