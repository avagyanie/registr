from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth.forms import SetPasswordForm
from .validators import CustomPasswordValidator
from django.core.exceptions import ValidationError
from login.models import Profile
from django.utils.text import slugify
from random import choice
import re


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email address'}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'id': 'password1'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'id': 'password2'}))
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    tel = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Telephone Number'}))

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password1", "password2"]

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        CustomPasswordValidator().validate(password1)
        count_lower = sum(1 for c in password1 if c.islower())
        count_upper = sum(1 for c in password1 if c.isupper())
        count_symbol = sum(1 for c in password1 if not c.isalnum())
        
        if count_lower < 3 or count_upper < 3 or count_symbol < 3:
            raise ValidationError("Password must contain a minimum of 3 uppercase, 3 lowercase, and 3 symbols.")
            
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match.")

        return password2

    def generate_username(self, first_name, last_name, tel):
        base_username = slugify(f"{first_name[choice(range(len(first_name)))]}{first_name[choice(range(len(first_name)))]}{first_name[choice(range(len(first_name)))]}{last_name[choice(range(len(last_name)))]}{last_name[choice(range(len(last_name)))]}{last_name[choice(range(len(last_name)))]}{tel[choice(range(len(tel)))]}{tel[choice(range(len(tel)))]}{tel[choice(range(len(tel)))]}")
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        return username
    
    def clean_tel(self):
        tel = self.cleaned_data.get('tel')
        if not re.match(r'^09\d{7}$', tel):
            raise ValidationError("Telephone number must be in the format 091111111.")
        if Profile.objects.filter(tel=tel).exists():
            raise ValidationError("This tel number is already registered.")
        return tel
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.generate_username(user.first_name, user.last_name, self.cleaned_data['tel'])

        if commit:
            user.save()

        profile, created = Profile.objects.get_or_create(user=user)
        profile.first_name = user.first_name
        profile.last_name = user.last_name
        profile.tel = self.cleaned_data['tel']
        profile.save()

        return user


class ProfileForm(forms.ModelForm):
    
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'clearablefileinput'}), label='Profile picture')

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'tel', 'address',  'image', 'birthday']
        widgets = {
            'birthday': forms.SelectDateWidget(years=range(1935, 2016))
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        
        self.instance.user.first_name = self.cleaned_data['first_name']
        self.instance.user.last_name = self.cleaned_data['last_name']

        profile = super(ProfileForm, self).save(commit=commit)

        if commit:
            self.instance.user.save()

        return profile


class PasswordChangeForm(SetPasswordForm):
    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'autocomplete': 'off'}),
    )

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        user = self.user
        if user.check_password(old_password):
            return old_password
        else:
            raise forms.ValidationError("Your old password is incorrect.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })
