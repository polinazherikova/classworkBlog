from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post,Subscriber,Comment, User,Profile

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        exclude=('published_date', 'user')

form=PostForm()
print(form)

class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ('email',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author','text')



class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['avatar','username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            if 'avatar' in self.cleaned_data and self.cleaned_data['avatar']:
                Profile.objects.create(user=user,avatar=self.cleaned_data['avatar'])
        return user

class ProfileUpdateForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)
    class Meta:
        model = Profile
        fields = ['avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField(initial=self.instance.user.username)
        self.fields['email'] = forms.EmailField(initial=self.instance.user.email)

    def save(self, commit=True):
        profile = super().save(commit=False)

        if 'avatar' in self.cleaned_data and self.cleaned_data['avatar']:
            profile.avatar = self.cleaned_data['avatar']
            if commit:
                profile.user.username = self.cleaned_data['username']
                profile.user.email = self.cleaned_data['email']
                profile.user.save()
                profile.save()
        return profile

