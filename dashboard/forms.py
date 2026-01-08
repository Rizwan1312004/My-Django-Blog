from django import forms
from blogs.models import Category, Blog
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        exclude = ['author', 'slug', 'created_at', 'updated_at']

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'is_staff',
            'is_active',
            'groups',
        ]
        error_messages = {
            'username': {
                'unique': "A user with that username already exists.",
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['groups'].required = False

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'is_active',
            'groups',
        ]
        error_messages = {
            'username': {
                'unique': "A user with that username already exists.",
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['groups'].required = False