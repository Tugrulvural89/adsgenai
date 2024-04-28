from django import forms
from .models import Contact, BusinessInquiry


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'content']


class BusinessInquiryForm(forms.ModelForm):
    class Meta:
        model = BusinessInquiry
        fields = ['user_description', 'ad_product']
