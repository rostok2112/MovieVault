import datetime
from dateutil.relativedelta import relativedelta
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils.safestring import mark_safe

from app.models import Actor, Director, Movie
from app.widgets import ImageWidget

class ReadOnlyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True
class BaseForm(forms.ModelForm):
    disabled_fields    = []
    add_hidden_fields  = []
    edit_hidden_fields = []
    
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name in self.disabled_fields:
            self.fields[field_name].disabled = True
        
        if not kwargs.get('instance'): # adding new
            for field_name in self.add_hidden_fields:
                self.fields.pop(field_name)   
        else:
            for field_name in self.edit_hidden_fields:
                self.fields.pop(field_name)
       

class MovieForm(BaseForm):
    logo = forms.CharField(widget=ImageWidget, required=False, )
    release_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    add_hidden_fields  = ['logo', ]
    disabled_fields  = ['logo', ]
    
    class Meta:
        model = Movie
        fields = [
            'title', 'release_date', 'director', 'actors', 'logo_url', 
        ]

    def __init__(self, *args, request=None,**kwargs):
        super(MovieForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance'):
            self.fields['logo'].initial = self.instance.logo_url

class ActorForm(BaseForm):
    add_hidden_fields  = ['age', ]
    disabled_fields = ['age',]
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    age = forms.IntegerField()
    
    def __init__(self, *args, **kwargs):
        super(ActorForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance'): # editing
            self.fields['age'].initial = (
                relativedelta(
                    datetime.date.today(), 
                    self.instance.date_of_birth
                )
            ).years if self.instance.date_of_birth else 0
    class Meta:
        model = Actor
        fields = [
            'name', 'surname', 'date_of_birth',
        ]
class DirectorForm(BaseForm):
    add_hidden_fields  = ['age', ]
    disabled_fields = ['age',]
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    age = forms.IntegerField()
    
    def __init__(self, *args, **kwargs):
        super(DirectorForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance'): # editing
            self.fields['age'].initial = (
                relativedelta(
                    datetime.date.today(), 
                    self.instance.date_of_birth
                )
            ).years if self.instance.date_of_birth else 0
        
    class Meta:
        model = Director
        fields = [
            'name', 'surname', 'date_of_birth'
        ]    


class CustomUserChangeForm(UserChangeForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput, required=False)
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput, required=False)
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password', None)
    
    def save(self, commit=True):
        user = super().save(commit=False)
        old_password = self.cleaned_data["old_password"]
        new_password = self.cleaned_data["new_password1"]

        if new_password:
            user.set_password(new_password)
        elif not new_password and old_password:
            raise forms.ValidationError("No new password provided.")
        elif not new_password and not old_password and not user.has_usable_password():
            user.password = self.initial["password"]

        if commit:
            user.save()
        return user

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if old_password and not self.instance.check_password(old_password):
            raise forms.ValidationError("Old password is incorrect.")
        return old_password

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("New passwords do not match.")
        
        validate_password(new_password2, self.instance)
        return new_password2
