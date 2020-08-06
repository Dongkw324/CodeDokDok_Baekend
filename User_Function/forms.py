from django import forms
from django.db import Users

class UsersForm(forms.ModelForm):
    class Meta:
        model=Users
        fields=('user_id')