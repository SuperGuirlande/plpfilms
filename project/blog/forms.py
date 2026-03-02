from django import forms
from .models import BlogCategory, BlogTag, BlogPost

INPUT  = 'w-full bg-gris-fonce border border-[#3a3a3a] focus:border-or text-blanc-casse placeholder-blanc-casse/30 font-texte text-sm px-4 py-3 outline-none transition-colors duration-200'
SELECT = 'w-full bg-gris-fonce border border-[#3a3a3a] focus:border-or text-blanc-casse font-texte text-sm px-4 py-3 outline-none transition-colors duration-200 cursor-pointer'
MULTI  = 'w-full bg-gris-fonce border border-[#3a3a3a] focus:border-or text-blanc-casse font-texte text-sm px-3 py-2 outline-none transition-colors duration-200 min-h-[100px]'
CHECK  = 'w-4 h-4 accent-or'


class BlogCategoryForm(forms.ModelForm):
    slug = forms.SlugField(
        required=False,
        widget=forms.TextInput(attrs={'class': INPUT, 'placeholder': 'Laissez vide pour auto-générer'}),
    )

    class Meta:
        model  = BlogCategory
        fields = ['name', 'slug', 'description']
        widgets = {
            'name':        forms.TextInput(attrs={'class': INPUT, 'placeholder': 'Cinéma'}),
            'description': forms.Textarea(attrs={'class': INPUT, 'rows': 3, 'placeholder': 'Description de la catégorie…'}),
        }


class BlogTagForm(forms.ModelForm):
    slug = forms.SlugField(
        required=False,
        widget=forms.TextInput(attrs={'class': INPUT, 'placeholder': 'Laissez vide pour auto-générer'}),
    )

    class Meta:
        model  = BlogTag
        fields = ['name', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT, 'placeholder': 'Court-métrage'}),
        }


class BlogPostForm(forms.ModelForm):
    slug             = forms.SlugField(required=False, widget=forms.TextInput(attrs={'class': INPUT, 'placeholder': 'Laissez vide pour auto-générer'}))
    meta_title       = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': INPUT, 'placeholder': 'Titre SEO (max 60 car.) — laissez vide pour utiliser le titre'}))
    meta_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': INPUT, 'rows': 3, 'placeholder': 'Description SEO (max 160 car.) — laissez vide pour utiliser l\'extrait'}))

    class Meta:
        model  = BlogPost
        fields = [
            'title', 'slug', 'category', 'tags', 'author', 'cover',
            'excerpt', 'content', 'status', 'is_featured',
            'meta_title', 'meta_description', 'published_at',
        ]
        widgets = {
            'title':        forms.TextInput(attrs={'class': INPUT, 'placeholder': 'Titre de l\'article'}),
            'category':     forms.Select(attrs={'class': SELECT}),
            'tags':         forms.SelectMultiple(attrs={'class': MULTI}),
            'author':       forms.Select(attrs={'class': SELECT}),
            'excerpt':      forms.Textarea(attrs={'class': INPUT, 'rows': 3, 'placeholder': 'Court résumé affiché dans la liste (max 300 car.)…'}),
            'status':       forms.Select(attrs={'class': SELECT}),
            'is_featured':  forms.CheckboxInput(attrs={'class': CHECK}),
            'published_at': forms.DateTimeInput(attrs={'class': INPUT, 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
