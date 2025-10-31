from django import forms
from captcha.fields import CaptchaField

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'name',
            'required': True
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email',
            'required': True
        })
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'subject',
            'required': True
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'message',
            'cols': 30,
            'rows': 2,
            'required': True
        })
    )
    captcha = CaptchaField()
