from django import forms
from .models import ContactMessage

INPUT    = 'w-full bg-noir-doux border border-gris-fonce focus:border-or text-blanc-casse placeholder-blanc-casse/30 font-texte text-sm px-5 py-4 outline-none transition-colors duration-200'
TEXTAREA = 'w-full bg-noir-doux border border-gris-fonce focus:border-or text-blanc-casse placeholder-blanc-casse/30 font-texte text-sm px-5 py-4 outline-none transition-colors duration-200 resize-none'


class ContactForm(forms.ModelForm):
    class Meta:
        model  = ContactMessage
        fields = ['first_name', 'last_name', 'email', 'phone', 'message']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': INPUT, 'placeholder': 'Votre prénom',
            }),
            'last_name': forms.TextInput(attrs={
                'class': INPUT, 'placeholder': 'Votre nom',
            }),
            'email': forms.EmailInput(attrs={
                'class': INPUT, 'placeholder': 'votre@email.com',
            }),
            'phone': forms.TextInput(attrs={
                'class': INPUT, 'placeholder': '06 XX XX XX XX — optionnel',
            }),
            'message': forms.Textarea(attrs={
                'class': TEXTAREA, 'rows': 6,
                'placeholder': 'Décrivez votre projet ou votre demande…',
            }),
        }
        labels = {
            'first_name': 'Prénom',
            'last_name':  'Nom',
            'email':      'Email',
            'phone':      'Téléphone',
            'message':    'Message',
        }
