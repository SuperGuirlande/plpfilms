from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from portfolio.models import PortfolioEntry
from blog.models import BlogPost
from .models import ContactMessage
from .forms import ContactForm


def home(request):
    # ── Formulaire de contact (POST) ──────────────
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre message a bien été envoyé. Pierrick vous répondra sous 48h.')
            return redirect(reverse('main:home') + '#contact')
        # En cas d'erreur, on repasse le form invalide à la page
    else:
        form = ContactForm()

    # ── Contexte ──────────────────────────────────
    portfolio_entries = PortfolioEntry.objects.filter(
        is_published=True
    ).select_related('category').order_by('-created_at')[:7]

    blog_posts = BlogPost.objects.filter(
        status='published'
    ).select_related('category', 'author').order_by('-published_at')[:3]

    return render(request, 'main/pages/home.html', {
        'portfolio_entries': portfolio_entries,
        'has_portfolio':     portfolio_entries.exists(),
        'blog_posts':        blog_posts,
        'has_blog':          blog_posts.exists(),
        'contact_form':      form,
    })
