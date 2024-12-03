# forms.py
from django import forms


class ImportForm(forms.Form):
    excel_file = forms.FileField()
