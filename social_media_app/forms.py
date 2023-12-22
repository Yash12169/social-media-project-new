from django import forms
from .models import UserProfile,Profile,Post

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['profilepic']


class DiscriptionChangeForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['discription']

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['media', 'discription']

    discription = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter description here'}),
        label='Custom Label for Description'
    )

class UserSearchForm(forms.ModelForm):
    search_query = forms.CharField(max_length=100)

