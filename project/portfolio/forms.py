from django import forms
from .models import PortfolioCategory, PortfolioEntry, PortfolioVideo

INPUT   = 'w-full bg-gris-fonce border border-[#3a3a3a] focus:border-or text-blanc-casse placeholder-blanc-casse/30 font-texte text-sm px-4 py-3 outline-none transition-colors duration-200'
SELECT  = 'w-full bg-gris-fonce border border-[#3a3a3a] focus:border-or text-blanc-casse font-texte text-sm px-4 py-3 outline-none transition-colors duration-200 cursor-pointer'
CHECK   = 'w-4 h-4 accent-or'


class PortfolioCategoryForm(forms.ModelForm):
    # Slug auto-généré côté vue si laissé vide
    slug = forms.SlugField(
        required=False,
        widget=forms.TextInput(attrs={'class': INPUT, 'placeholder': 'Laissez vide pour auto-générer'}),
    )

    class Meta:
        model  = PortfolioCategory
        fields = ['name', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT, 'placeholder': 'Court-métrage'}),
        }


class PortfolioEntryForm(forms.ModelForm):
    # Slug auto-généré côté vue si laissé vide
    slug = forms.SlugField(
        required=False,
        widget=forms.TextInput(attrs={'class': INPUT, 'placeholder': 'Laissez vide pour auto-générer'}),
    )

    class Meta:
        model  = PortfolioEntry
        fields = ['title', 'slug', 'category', 'thumbnail', 'short_description', 'content', 'is_published']
        widgets = {
            'title':             forms.TextInput(attrs={'class': INPUT, 'placeholder': 'Titre du projet'}),
            'category':          forms.Select(attrs={'class': SELECT}),
            'short_description': forms.Textarea(attrs={'class': INPUT, 'rows': 3, 'placeholder': 'Description courte affichée dans la grille…'}),
            'is_published':      forms.CheckboxInput(attrs={'class': CHECK}),
        }


class PortfolioVideoForm(forms.ModelForm):
    # Champs optionnels explicitement marqués
    title       = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': INPUT, 'placeholder': 'Titre de la vidéo (optionnel)'}),
    )
    youtube_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'class': INPUT, 'placeholder': 'https://www.youtube.com/watch?v=…'}),
    )

    class Meta:
        model  = PortfolioVideo
        fields = ['title', 'video_type', 'youtube_url', 'file', 'order']
        widgets = {
            'video_type': forms.Select(attrs={'class': SELECT}),
            'order':      forms.NumberInput(attrs={'class': INPUT}),
        }


# Formset inline pour les vidéos dans le formulaire d'entrée
PortfolioVideoFormSet = forms.inlineformset_factory(
    PortfolioEntry,
    PortfolioVideo,
    form=PortfolioVideoForm,
    extra=1,
    can_delete=True,
)
