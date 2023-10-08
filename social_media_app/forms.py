from django import forms
class Profile(forms.Form):
    profilepic=forms.ImageField()
    discription=forms.CharField()