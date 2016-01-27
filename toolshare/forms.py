"""
    File:       mysite/toolshare/forms.py
    Language:   Python 2.7 with Django Web Framework

    Author:     Larwan Berke      <lwb2627@rit.edu>
    Author:     Mitayshh Dhaggai  <mxd3549@rit.edu>
    Author:     Arun Gopinathan   <ag7941@rit.edu>
    Author:     Noella Kolash     <nak8595@rit.edu>
    Author:     Andrew Marone     <agm1392@rit.edu>

    File Description: The forms we need for this toolshare project.
    """
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

from toolshare.models import TSUser
from toolshare.models import Tool, Shed, BorrowTransaction

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, max_length=100)

class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, min_length=3, max_length=100)
    reTypePassword = forms.CharField(label='Retype Password', widget=forms.PasswordInput, min_length=3, max_length=100)
    name = forms.CharField(label='Name', max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class': 'form-control'}))
    zipcode = forms.IntegerField(min_value=10000,widget=forms.TextInput(attrs={'class': 'form-control'}))

    widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'reTypePassword': forms.PasswordInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
    }

    # block registering when username exists
    def get_username(self):
        u = self.cleaned_data['username']
        try:
            User.objects.get(username=u)
        except User.DoesNotExist:
            return u
        raise forms.ValidationError('Username taken')

    # same thing with email
    def get_email(self):
        e = self.cleaned_data['email']
        try:
            User.objects.get(email=e)
        except User.DoesNotExist:
            return e
        raise forms.ValidationError('E-mail address taken')

    # generic attrs
    def get_password(self):
        return self.cleaned_data['password']

    def isPasswordCorrect(self):
        password = self.cleaned_data['password']
        reTypePassword = self.cleaned_data['reTypePassword']

        if password == reTypePassword:
            return True
        else:
            return False

    def get_zipcode(self):
        return self.cleaned_data['zipcode']

    def get_name(self):
        return self.cleaned_data['name']

    def get_address(self):
        return self.cleaned_data['address']

class RegistrationDetailsForm(RegisterForm):

     def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields.pop('username')
        self.fields.pop('password')
        self.fields.pop('reTypePassword')

# ChangePasswordForm should have been a subclass of RegisterForm.
# But could not ORDER the fields
class ChangePasswordForm(forms.Form):

    currentPassword = forms.CharField(label='Current Password', widget=forms.PasswordInput(attrs={'class': 'form-control','style': 'width:30%'}), min_length=3, max_length=100)
    newPassword = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class': 'form-control','style': 'width:30%'}), min_length=3, max_length=100)
    reTypeNewPassword = forms.CharField(label='Retype New Password', widget=forms.PasswordInput(attrs={'class': 'form-control','style': 'width:30%'}), min_length=3, max_length=100)

    widgets = {
            'currentPassword': forms.PasswordInput(attrs={'class': 'form-control',}),
            'newPassword': forms.PasswordInput(attrs={'class': 'form-control'}),
            'reTypeNewPassword': forms.PasswordInput(attrs={'class': 'form-control'}),
    }

    def get_currentPassword(self):
        return self.cleaned_data['currentPassword']

    def get_newPassword(self):
        return self.cleaned_data['newPassword']

    def get_reTypeNewPassword(self):
        return self.cleaned_data['reTypeNewPassword']

    def isNewPasswordCorrect(self):

        if self.get_newPassword() == self.get_reTypeNewPassword():
            return True
        else:
            return False


class ToolRegistration(ModelForm):

    toolImage = forms.ImageField(required=False)

    class Meta:
        model = Tool

        fields = ['name', 'shareLocation', 'toolDescription', 'toolImage', 'blackout_start', 'blackout_end']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'shareLocation': forms.Select(attrs={'class': 'form-control'}),
            'toolDescription': forms.TextInput(attrs={'class': 'form-control'}),
            'blackout_start': forms.HiddenInput(),
            'blackout_end': forms.HiddenInput(),
        }

class ShedEditor(ModelForm):
    class Meta:
        model = Shed
        fields = ['name', 'address']

class BorrowTransactionEditor(ModelForm):
    class Meta:
        model = BorrowTransaction

        fields = ['borrowDate', 'dueDate', 'borrower_arrangements']

        widgets = {
            'borrowDate': forms.HiddenInput(),
            'dueDate': forms.HiddenInput(),
            'borrower_arrangements': forms.TextInput(attrs={'class': 'form-control'}),
        }

class BorrowTransactionOwnerEditor(ModelForm):
    class Meta:
        model = BorrowTransaction
        fields = ['owner_arrangements']

        widgets = {
            'owner_arrangements': forms.TextInput(attrs={'class': 'form-control'}),
        }
