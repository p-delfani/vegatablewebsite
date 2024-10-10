from django import forms
from .models import ContactUs


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ('name', 'email', 'subject', 'text')

        widgets = {
            'name': forms.TextInput(attrs={
                'id': "name",
                'class': 'form-control',
                'placeholder': 'نام'
            }),

            'email': forms.EmailInput(attrs={
                'id': "email",
                'class': 'form-control',
                'placeholder': 'ایمیل'
            }),

            'subject': forms.TextInput(attrs={
                'id': "subject",
                'class': 'form-control',
                'placeholder': 'موضوع'
            }),

            'text': forms.Textarea(attrs={
                'id': "message",
                'class': 'form-control w-100',
                'placeholder': 'پیام'
            })
        }

