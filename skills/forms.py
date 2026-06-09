from django import forms
from .models import Rating
from django.contrib.auth.forms import UserCreationForm
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'review']


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):

    ROLE_CHOICES = [
        ('learner', 'Learner'),
        ('teacher', 'Teacher'),
    ]

    email = forms.EmailField()

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect
    )

    skill = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'role',
            'skill'
        ]
   
class RequestOTPForm(forms.Form):
    email = forms.EmailField(label="Enter your email")

class VerifyOTPForm(forms.Form):
    email = forms.EmailField(widget=forms.HiddenInput())
    otp = forms.CharField(max_length=10, label="Enter OTP")