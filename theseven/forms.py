from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import Textarea, TextInput, EmailInput, NumberInput, FileInput

from .models import Comment, Post, Profile, Reply
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', 'comment_pic')
        widgets = {
            'body': Textarea(attrs={
                'style': 'border-radius:7px; width:100%; font-size:14px; padding:4px; border:1px solid grey;',
                'placeholder': 'Write a comment',
                'rows': '4'}),
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('body', 'comment_pic')
        widgets = {'body': Textarea(
            attrs={'class': 'form-control', 'rows': '3', 'placeholder': "Write a reply to this comment"})}


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'post_pic')
        widgets = {
            'title': Textarea(attrs={'class': 'form-control is_invalid', 'rows': '1', 'placeholder': 'Headline', 'style':'font-size:15px'}),
            'content': Textarea(attrs={'class': 'form-control', 'placeholder': 'Body', 'style':'font-size:15px'})}


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'dp', 'gender', 'birthday', 'country', 'state', 'bio','job'
        )

        widgets = {
            'dp': FileInput(),
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'first_name'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'last_name'}),
            'birthday': TextInput(attrs={'class': 'form-control'}),
            'job': TextInput(attrs={'class': 'form-control'}),
            'occupation': TextInput(attrs={'class': 'form-control'}),
            'state': TextInput(attrs={'class': 'form-control', 'placeholder': 'state'}),
            'country': TextInput(attrs={'class': 'form-control', 'placeholder': 'country'}),
            'bio': TextInput(attrs={'class': 'form-control', 'placeholder': 'Talk about yourself or your skill'}),
            'twitter': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter your twitter username (optional)'}),
            'facebook': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter link to your facebook profile (optional)'}),
            'linkedin': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter link to your linkedin profile (optional)'}),
            'instagram': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter link to your instagram profile (optional)'}),
        }


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# User update form allows users to update user name and email
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'username'}),
        }
