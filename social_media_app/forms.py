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


# class CreatePostForm(forms.ModelForm):
#     class Meta:
#         model=Post
#         fields=['media','discription']
#         widgets = {
#             'discription': forms.Textarea(attrs={'placeholder': 'Enter description here'}),
            
#         }



class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['media', 'discription']

    discription = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter description here'}),
        label='Custom Label for Description'
    )