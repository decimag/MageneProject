from django import forms
from MageneApp.models import ACTES,GENUSERS_PROFIL
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,PasswordResetForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    username=forms.CharField(label="login")
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','last_name','first_name']

class ResetPwd(PasswordResetForm):
    email = forms.CharField(label="email")
    class Meta:
        model = User
        fields = ['email']

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = ACTES
        fields = ['IMG_ACTES']

class MariageForm(forms.ModelForm):
    class Meta:
        model = ACTES
        fields = ['NOM1','NOM2','PRENOM1','PRENOM2','IMG_ACTES','NUMPART_ACTE','DATE_ACTE','LINKACTE','TYPE','DATE','LOGIN','INTITULE']

class ProfilePlus(forms.ModelForm):
    class Meta:
        model = GENUSERS_PROFIL
        fields = ['WEBSITE']

class UserPlus(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','username']





