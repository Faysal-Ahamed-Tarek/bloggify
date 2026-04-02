from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from blog.models import Comments
    

class registration(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text="First name")
    last_name = forms.CharField(max_length=30, required=True, help_text="Last name")
    email = forms.EmailField(max_length=254, required=True, help_text="Email address")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.pop("autofocus", None)
        self.fields["first_name"].widget.attrs["autofocus"] = True

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email address already exists.")
        return email


    def save(self, commit=True) : 
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user



class commentForm(forms.ModelForm) : 
    content = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), max_length=1000, required=True, help_text="Write your comment here.")

    class Meta:
        model = Comments
        fields = ["content"]
