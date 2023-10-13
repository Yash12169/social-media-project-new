from django import forms
from .models import UserProfile,Profile

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['profilepic']


class DiscriptionChangeForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['discription']


        