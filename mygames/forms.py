from django import forms
from .models import Games


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username', 'placeholder': 'Enter Username'}))
    password = forms.CharField(label='Password', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password', 'placeholder': 'Enter Password', 'type': 'password'}))
# forms.ModelMultipleChoiceField(queryset=Author.objects.all())


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username', 'placeholder': 'Enter Your Username'}))
    password = forms.CharField(label='Password', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password', 'placeholder': 'Enter Your Password', 'type': 'password'}))
    confirmPassword = forms.CharField(label='Password', max_length=100,
                                      widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'confirmPassword', 'placeholder': 'Re-enter Your Password', 'type': 'password'}))
    email = forms.CharField(label='Email', max_length=100,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'email', 'placeholder': 'Enter Your Email'}))
    games = forms.ModelMultipleChoiceField(queryset=Games.objects.all())
    favourite = forms.ModelMultipleChoiceField(queryset=Games.objects.all())


class AddGameForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'name', 'placeholder': 'Enter Game Name'}))
    category = forms.CharField(label='category', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'category', 'placeholder': 'Enter Your Category'}))
    url = forms.CharField(label='url', max_length=100,
                          widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'url', 'placeholder': 'Enter Game URL'}))
    imagepath = forms.CharField(label='Image Path', max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'imagepath', 'placeholder': 'Enter Game Image URL'}))
    description = forms.CharField(label='Description', max_length=300,
                                  widget=forms.Textarea(attrs={'class': 'form-control', 'name': 'description', 'placeholder': 'Enter Game description'}))


class postForm(forms.Form):
    # queryset = Games.objects.all())
    game = forms.ModelMultipleChoiceField(
        queryset=Games.objects.all())  # .values('name').last())
    title = forms.CharField(label='Name', max_length=100,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'name', 'placeholder': 'enter title for the post'}))
    description = forms.CharField(label='Description', max_length=300,
                                  widget=forms.Textarea(attrs={'class': 'form-control', 'name': 'description', 'placeholder': 'Enter Game description'}))
    playerno = forms.ChoiceField(
        choices=((1, "2-3"), (2, "2-5"), (3, "4-10")))
    request_duration = forms.ChoiceField(
        choices=((1, "1 hour min -3 hours max"), (2, "2 hour min -5 hours max")))
    request_status = forms.BooleanField(required=False)
    message_status = forms.BooleanField(required=False)


class settingForm(forms.Form):
    can_Message = forms.BooleanField()
    can_Search = forms.BooleanField()


class messageForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter your username'}))
    email = forms.CharField(label='Email', max_length=100,
                            widget=forms.TextInput(attrs={'class': 'form-control',  'placeholder': 'Enter Your Email'}))
    message = forms.CharField(label='Message', max_length=300,
                              widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'message'}))
