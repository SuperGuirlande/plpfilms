from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils.text import slugify

from .models import PortfolioCategory, PortfolioEntry, PortfolioVideo
from .forms import PortfolioCategoryForm, PortfolioEntryForm, PortfolioVideoFormSet

superuser_required = user_passes_test(lambda u: u.is_superuser, login_url='accounts:login')


# ─────────────────────────────────────────────
#  VUES PUBLIQUES
# ─────────────────────────────────────────────

def portfolio_list(request):
    category_slug = request.GET.get('categorie')
    categories    = PortfolioCategory.objects.filter(entries__is_published=True).distinct()
    entries       = PortfolioEntry.objects.filter(is_published=True).select_related('category').order_by('-created_at')

    active_category = None
    if category_slug:
        active_category = get_object_or_404(PortfolioCategory, slug=category_slug)
        entries = entries.filter(category=active_category)

    return render(request, 'portfolio/portfolio_list.html', {
        'entries':         entries,
        'categories':      categories,
        'active_category': active_category,
    })


def portfolio_detail(request, slug):
    entry    = get_object_or_404(PortfolioEntry, slug=slug, is_published=True)
    videos   = entry.videos.all()
    # Navigation prev / next
    qs      = PortfolioEntry.objects.filter(is_published=True).order_by('-created_at')
    ids     = list(qs.values_list('id', flat=True))
    idx     = ids.index(entry.id)
    prev_entry = qs.filter(id=ids[idx + 1]).first() if idx + 1 < len(ids) else None
    next_entry = qs.filter(id=ids[idx - 1]).first() if idx > 0 else None

    return render(request, 'portfolio/portfolio_detail.html', {
        'entry':      entry,
        'videos':     videos,
        'prev_entry': prev_entry,
        'next_entry': next_entry,
    })


# ─────────────────────────────────────────────
#  CATÉGORIES
# ─────────────────────────────────────────────

@login_required
@superuser_required
def admin_category_list(request):
    categories = PortfolioCategory.objects.all()
    return render(request, 'portfolio/admin/category_list.html', {
        'categories': categories,
        'admin_section': 'categories',
    })


@login_required
@superuser_required
def admin_category_create(request):
    form = PortfolioCategoryForm(request.POST or None)
    if form.is_valid():
        category = form.save(commit=False)
        if not category.slug:
            category.slug = slugify(category.name)
        category.save()
        messages.success(request, f'Catégorie « {category.name} » créée.')
        return redirect('portfolio:admin_category_list')
    return render(request, 'portfolio/admin/category_form.html', {
        'form': form,
        'action': 'Créer',
        'admin_section': 'categories',
    })


@login_required
@superuser_required
def admin_category_edit(request, pk):
    category = get_object_or_404(PortfolioCategory, pk=pk)
    form = PortfolioCategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        messages.success(request, f'Catégorie « {category.name} » modifiée.')
        return redirect('portfolio:admin_category_list')
    return render(request, 'portfolio/admin/category_form.html', {
        'form': form,
        'object': category,
        'action': 'Modifier',
        'admin_section': 'categories',
    })


@login_required
@superuser_required
def admin_category_delete(request, pk):
    category = get_object_or_404(PortfolioCategory, pk=pk)
    if request.method == 'POST':
        name = category.name
        category.delete()
        messages.success(request, f'Catégorie « {name} » supprimée.')
        return redirect('portfolio:admin_category_list')
    return render(request, 'portfolio/admin/confirm_delete.html', {
        'object': category,
        'object_type': 'la catégorie',
        'cancel_url': 'portfolio:admin_category_list',
        'admin_section': 'categories',
    })


# ─────────────────────────────────────────────
#  ENTRÉES PORTFOLIO
# ─────────────────────────────────────────────

@login_required
@superuser_required
def admin_entry_list(request):
    entries = PortfolioEntry.objects.select_related('category').prefetch_related('videos')
    return render(request, 'portfolio/admin/entry_list.html', {
        'entries': entries,
        'admin_section': 'portfolio',
    })


@login_required
@superuser_required
def admin_entry_create(request):
    form    = PortfolioEntryForm(request.POST or None, request.FILES or None)
    formset = PortfolioVideoFormSet(request.POST or None, request.FILES or None)

    if form.is_valid() and formset.is_valid():
        entry = form.save(commit=False)
        if not entry.slug:
            entry.slug = slugify(entry.title)
        entry.save()
        formset.instance = entry
        formset.save()
        messages.success(request, f'Entrée « {entry.title} » créée.')
        return redirect('portfolio:admin_entry_list')

    return render(request, 'portfolio/admin/entry_form.html', {
        'form': form,
        'formset': formset,
        'action': 'Créer',
        'admin_section': 'portfolio',
    })


@login_required
@superuser_required
def admin_entry_edit(request, pk):
    entry   = get_object_or_404(PortfolioEntry, pk=pk)
    form    = PortfolioEntryForm(request.POST or None, request.FILES or None, instance=entry)
    formset = PortfolioVideoFormSet(request.POST or None, request.FILES or None, instance=entry)

    if form.is_valid() and formset.is_valid():
        form.save()
        formset.save()
        messages.success(request, f'Entrée « {entry.title} » modifiée.')
        return redirect('portfolio:admin_entry_list')

    return render(request, 'portfolio/admin/entry_form.html', {
        'form': form,
        'formset': formset,
        'object': entry,
        'action': 'Modifier',
        'admin_section': 'portfolio',
    })


@login_required
@superuser_required
def admin_entry_delete(request, pk):
    entry = get_object_or_404(PortfolioEntry, pk=pk)
    if request.method == 'POST':
        title = entry.title
        entry.delete()
        messages.success(request, f'Entrée « {title} » supprimée.')
        return redirect('portfolio:admin_entry_list')
    return render(request, 'portfolio/admin/confirm_delete.html', {
        'object': entry,
        'object_type': "l'entrée portfolio",
        'cancel_url': 'portfolio:admin_entry_list',
        'admin_section': 'portfolio',
    })
