from django import forms
from django.contrib.auth.models import User, Group
from general.models import Sections
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm

class CustomUserChangeForm(UserChangeForm):
    new_password1 = forms.CharField(label="Nowe hasło", widget=forms.PasswordInput, required=False)
    new_password2 = forms.CharField(label="Potwierdź nowe hasło", widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'new_password1', 'new_password2')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 and password1 != password2:
            self.add_error('new_password2', "Hasła nie są identyczne.")

class ExtendedUserChangeForm(CustomUserChangeForm):
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(),required=False, widget=forms.SelectMultiple(attrs={'class': 'select2'}))
    sections = forms.ModelMultipleChoiceField(queryset=Sections.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'class': 'select2'}))
    
    class Meta(CustomUserChangeForm.Meta):
        fields = CustomUserChangeForm.Meta.fields + ('groups', 'sections',)

class CustomPasswordChangeForm(PasswordChangeForm):
    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        if len(password) < 12 or len(password) > 128:
            raise forms.ValidationError("Password must be between 12 and 128 characters.")
        return password
