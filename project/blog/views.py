from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils.text import slugify
from django.db.models import Q

from .models import BlogCategory, BlogTag, BlogPost
from .forms import BlogCategoryForm, BlogTagForm, BlogPostForm

superuser_required = user_passes_test(lambda u: u.is_superuser, login_url='accounts:login')


# ═══════════════════════════════════════════════
#  VUES PUBLIQUES
# ═══════════════════════════════════════════════

def blog_list(request):
    posts      = BlogPost.objects.filter(status='published').select_related('category', 'author').prefetch_related('tags').order_by('-published_at')
    categories = BlogCategory.objects.filter(posts__status='published').distinct()
    tags       = BlogTag.objects.filter(posts__status='published').distinct()
    featured   = posts.filter(is_featured=True).first()

    # Filtres
    category_slug = request.GET.get('categorie')
    tag_slug      = request.GET.get('tag')
    search_query  = request.GET.get('q', '').strip()

    active_category = None
    active_tag      = None

    if category_slug:
        active_category = get_object_or_404(BlogCategory, slug=category_slug)
        posts = posts.filter(category=active_category)
        featured = None

    if tag_slug:
        active_tag = get_object_or_404(BlogTag, slug=tag_slug)
        posts = posts.filter(tags=active_tag)
        featured = None

    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )
        featured = None

    # Exclure le featured de la liste principale pour éviter le doublon
    if featured:
        posts = posts.exclude(pk=featured.pk)

    return render(request, 'blog/blog_list.html', {
        'posts':           posts,
        'featured':        featured,
        'categories':      categories,
        'tags':            tags,
        'active_category': active_category,
        'active_tag':      active_tag,
        'search_query':    search_query,
    })


def blog_detail(request, slug):
    post    = get_object_or_404(BlogPost, slug=slug, status='published')
    related = BlogPost.objects.filter(
        status='published', category=post.category
    ).exclude(pk=post.pk).order_by('-published_at')[:3]

    # Navigation prev / next
    qs  = BlogPost.objects.filter(status='published').order_by('-published_at')
    ids = list(qs.values_list('id', flat=True))
    idx = ids.index(post.id)
    prev_post = qs.filter(id=ids[idx + 1]).first() if idx + 1 < len(ids) else None
    next_post = qs.filter(id=ids[idx - 1]).first() if idx > 0 else None

    return render(request, 'blog/blog_detail.html', {
        'post':      post,
        'related':   related,
        'prev_post': prev_post,
        'next_post': next_post,
    })


# ═══════════════════════════════════════════════
#  ADMIN — CATÉGORIES
# ═══════════════════════════════════════════════

@login_required
@superuser_required
def admin_category_list(request):
    return render(request, 'blog/admin/category_list.html', {
        'categories':   BlogCategory.objects.all(),
        'admin_section': 'blog',
    })


@login_required
@superuser_required
def admin_category_create(request):
    form = BlogCategoryForm(request.POST or None)
    if form.is_valid():
        cat = form.save(commit=False)
        if not cat.slug:
            cat.slug = slugify(cat.name)
        cat.save()
        messages.success(request, f'Catégorie « {cat.name} » créée.')
        return redirect('blog:admin_category_list')
    return render(request, 'blog/admin/category_form.html', {
        'form': form, 'action': 'Créer', 'admin_section': 'blog',
    })


@login_required
@superuser_required
def admin_category_edit(request, pk):
    cat  = get_object_or_404(BlogCategory, pk=pk)
    form = BlogCategoryForm(request.POST or None, instance=cat)
    if form.is_valid():
        form.save()
        messages.success(request, f'Catégorie « {cat.name} » modifiée.')
        return redirect('blog:admin_category_list')
    return render(request, 'blog/admin/category_form.html', {
        'form': form, 'object': cat, 'action': 'Modifier', 'admin_section': 'blog',
    })


@login_required
@superuser_required
def admin_category_delete(request, pk):
    cat = get_object_or_404(BlogCategory, pk=pk)
    if request.method == 'POST':
        name = cat.name
        cat.delete()
        messages.success(request, f'Catégorie « {name} » supprimée.')
        return redirect('blog:admin_category_list')
    return render(request, 'blog/admin/confirm_delete.html', {
        'object': cat, 'object_type': 'la catégorie',
        'cancel_url': 'blog:admin_category_list', 'admin_section': 'blog',
    })


# ═══════════════════════════════════════════════
#  ADMIN — TAGS
# ═══════════════════════════════════════════════

@login_required
@superuser_required
def admin_tag_list(request):
    return render(request, 'blog/admin/tag_list.html', {
        'tags': BlogTag.objects.all(), 'admin_section': 'blog',
    })


@login_required
@superuser_required
def admin_tag_create(request):
    form = BlogTagForm(request.POST or None)
    if form.is_valid():
        tag = form.save(commit=False)
        if not tag.slug:
            tag.slug = slugify(tag.name)
        tag.save()
        messages.success(request, f'Tag « {tag.name} » créé.')
        return redirect('blog:admin_tag_list')
    return render(request, 'blog/admin/tag_form.html', {
        'form': form, 'action': 'Créer', 'admin_section': 'blog',
    })


@login_required
@superuser_required
def admin_tag_delete(request, pk):
    tag = get_object_or_404(BlogTag, pk=pk)
    if request.method == 'POST':
        name = tag.name
        tag.delete()
        messages.success(request, f'Tag « {name} » supprimé.')
        return redirect('blog:admin_tag_list')
    return render(request, 'blog/admin/confirm_delete.html', {
        'object': tag, 'object_type': 'le tag',
        'cancel_url': 'blog:admin_tag_list', 'admin_section': 'blog',
    })


# ═══════════════════════════════════════════════
#  ADMIN — ARTICLES
# ═══════════════════════════════════════════════

@login_required
@superuser_required
def admin_post_list(request):
    posts = BlogPost.objects.select_related('category', 'author').order_by('-created_at')
    return render(request, 'blog/admin/post_list.html', {
        'posts': posts, 'admin_section': 'blog',
    })


@login_required
@superuser_required
def admin_post_create(request):
    form = BlogPostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        if not post.slug:
            post.slug = slugify(post.title)
        if not post.author:
            post.author = request.user
        post.save()
        form.save_m2m()
        messages.success(request, f'Article « {post.title} » créé.')
        return redirect('blog:admin_post_list')
    return render(request, 'blog/admin/post_form.html', {
        'form': form, 'action': 'Créer', 'admin_section': 'blog',
    })


@login_required
@superuser_required
def admin_post_edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    form = BlogPostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        messages.success(request, f'Article « {post.title} » modifié.')
        return redirect('blog:admin_post_list')
    return render(request, 'blog/admin/post_form.html', {
        'form': form, 'object': post, 'action': 'Modifier', 'admin_section': 'blog',
    })


@login_required
@superuser_required
def admin_post_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        title = post.title
        post.delete()
        messages.success(request, f'Article « {title} » supprimé.')
        return redirect('blog:admin_post_list')
    return render(request, 'blog/admin/confirm_delete.html', {
        'object': post, 'object_type': "l'article",
        'cancel_url': 'blog:admin_post_list', 'admin_section': 'blog',
    })
