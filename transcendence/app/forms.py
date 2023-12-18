from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from api.imageValidation import validateFileType, validationImageSize
from django.core.files import File
from django.http import JsonResponse

from api.models import CustomUserData

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUserData
        fields = ('email',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUserData
        fields = ('email',)


# enforces our custom user table on users.
User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', "autocomplete": "on"}))


class SignupForm(CustomUserCreationForm):
    username = forms.CharField(label='Username',
        min_length=5,
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="email",
        widget=forms.EmailInput(attrs={"class": "form-control"}))
    coallition = forms.ChoiceField(choices=(
        ('builders', 'The Builders'),
        ('foragers', 'The Foragers'),
        ('guards', 'The Guards'),
    ), widget=forms.RadioSelect)
    password1 = forms.CharField(
        label='password',
        widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "on"})
    )
    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "on"})
    )

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        new = CustomUserData.objects.filter(username = username)
        if new.count():
            raise ValidationError("User Already Exist")
        return username

    def email_clean(self):
        email = self.cleaned_data['email'].lower()
        new = CustomUserData.objects.filter(email=email)
        if new.count():
            raise ValidationError("Email Already Exist")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        return password2

    def save(self, commit = True):
        user = CustomUserData.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        user.coallition = self.cleaned_data['coallition']
        f = open("app/static/images/profileIconWhite.png", "rb")
        djangoFile = File(f)
        user.avatarImage = djangoFile
        user.full_clean()
        user.save()
        f.close()
        return user


class ChangeProfile(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        min_length=5,
        max_length=100
        )
    firstName = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        )
    lastName = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}),
        required=False
        )
    password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(
        attrs={'class': 'form-control', "autocomplete": "on"}),
        required=False
    )
    password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', "autocomplete": "on"}),
        required=False
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    password3 = forms.CharField(
        label="Confirm your password to apply the changes",
        widget=forms.PasswordInput(attrs={'class': 'form-control', "autocomplete": "on"})
    )

    def isPasswordValid(self, userModel : CustomUserData):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            print("password1 and password2 does not match")
            return False, JsonResponse({"success": "false", "message": "Failed to update profile", "errors": {"password2": "New passwords don't match"}}, status=400)
        if check_password(self.cleaned_data['password3'], userModel.password) == False:
            print("Password provided does not match with the original one")
            return False, JsonResponse({"success": "false", "message": "Failed to update profile", "errors": {"password3": "Your current password is not correct"}}, status=400)
        return True, JsonResponse({"success": "true", "message": "profile updated successfuly"}, status=200)

    def save(self, userModel : CustomUserData):
        userModel.username = self.cleaned_data['username']
        userModel.first_name = self.cleaned_data['firstName']
        userModel.last_name = self.cleaned_data['lastName']
        if (len(self.cleaned_data['password1']) > 0):
            userModel.set_password(self.cleaned_data['password1'])
        userModel.email = self.cleaned_data['email']
        userModel.full_clean()
        userModel.save()

class ProfilePicture(forms.Form):

    avatarImage = forms.FileField(validators=[validationImageSize, validateFileType])

    def save(self, userModel : CustomUserData):
        if userModel.avatarImage:
            if default_storage.exists(userModel.avatarImage.name):
                default_storage.delete(userModel.avatarImage.name)
        userModel.avatarImage = self.cleaned_data['avatarImage']
        userModel.full_clean()
        userModel.save()

