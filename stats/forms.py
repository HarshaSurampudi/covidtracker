from django import forms
class Subscribe(forms.Form):
    phoneNumber = forms.CharField(label='Your Whatsapp Number', max_length=100, widget=forms.TextInput(attrs={'placeholder': '+919876543210'}))
