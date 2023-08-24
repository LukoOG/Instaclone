from .models import Post, Profile
from django.forms import ModelForm


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['profile', 'like']


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user', 'follows']
