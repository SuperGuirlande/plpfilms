from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

# Classes Tailwind réutilisables
INPUT_CLASS  = 'w-full bg-gris-fonce border border-[#3a3a3a] focus:border-or text-blanc-casse placeholder-blanc-casse/30 font-texte text-sm px-4 py-3 outline-none transition-colors duration-200'
LABEL_CLASS  = 'block font-sous-titre text-xs tracking-[2px] uppercase text-blanc-casse/60 mb-2'


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model  = CustomUser
        fields = ['email', 'username', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Adresse e-mail"),
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'exemple@email.com',
            'autofocus': True,
        }),
    )
    password = forms.CharField(
        label=_('Mot de passe'),
        widget=forms.PasswordInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': '••••••••',
        }),
    )


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label=_('Ancien mot de passe'),
        widget=forms.PasswordInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': '••••••••',
        }),
    )
    new_password = forms.CharField(
        label=_('Nouveau mot de passe'),
        widget=forms.PasswordInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': '••••••••',
        }),
    )
    confirm_password = forms.CharField(
        label=_('Confirmer le nouveau mot de passe'),
        widget=forms.PasswordInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': '••••••••',
        }),
    )
