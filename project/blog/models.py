import re
from django.db import models
from django.conf import settings
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field


class BlogCategory(models.Model):
    name        = models.CharField(max_length=100, verbose_name="Nom")
    slug        = models.SlugField(unique=True,    verbose_name="Slug")
    description = models.TextField(blank=True,     verbose_name="Description")

    class Meta:
        verbose_name        = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering            = ['name']

    def __str__(self):
        return self.name


class BlogTag(models.Model):
    name = models.CharField(max_length=50,  verbose_name="Nom")
    slug = models.SlugField(unique=True,    verbose_name="Slug")

    class Meta:
        verbose_name        = "Tag"
        verbose_name_plural = "Tags"
        ordering            = ['name']

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft',     'Brouillon'),
        ('published', 'Publié'),
    ]

    # ── Contenu ──────────────────────────────
    title    = models.CharField(max_length=200, verbose_name="Titre")
    slug     = models.SlugField(unique=True,    verbose_name="Slug")
    category = models.ForeignKey(
        BlogCategory, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='posts',
        verbose_name="Catégorie",
    )
    tags = models.ManyToManyField(
        BlogTag, blank=True, related_name='posts',
        verbose_name="Tags",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='blog_posts',
        verbose_name="Auteur",
    )
    cover = models.ImageField(
        upload_to='blog/covers/', blank=True, null=True,
        verbose_name="Image de couverture",
    )
    excerpt = models.CharField(
        max_length=300, verbose_name="Extrait",
        help_text="Court résumé affiché dans la liste (max 300 caractères).",
    )
    content = CKEditor5Field(verbose_name="Contenu", config_name='blog')

    # ── Publication ──────────────────────────
    status      = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft',
        verbose_name="Statut",
    )
    is_featured = models.BooleanField(
        default=False, verbose_name="Mis en avant",
        help_text="Affiché en tête de liste et sur la home.",
    )

    # ── SEO ──────────────────────────────────
    meta_title = models.CharField(
        max_length=60, blank=True, verbose_name="Meta title",
        help_text="Laissez vide pour utiliser le titre (max 60 car.).",
    )
    meta_description = models.CharField(
        max_length=160, blank=True, verbose_name="Meta description",
        help_text="Laissez vide pour utiliser l'extrait (max 160 car.).",
    )

    # ── Dates ────────────────────────────────
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="Publié le")
    created_at   = models.DateTimeField(auto_now_add=True,     verbose_name="Créé le")
    updated_at   = models.DateTimeField(auto_now=True,         verbose_name="Modifié le")

    class Meta:
        verbose_name        = "Article"
        verbose_name_plural = "Articles"
        ordering            = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    # ── Propriétés SEO ───────────────────────
    @property
    def effective_meta_title(self):
        return self.meta_title or self.title

    @property
    def effective_meta_description(self):
        return self.meta_description or self.excerpt

    # ── Temps de lecture estimé ──────────────
    @property
    def reading_time(self):
        """Estimation à 200 mots / minute."""
        text  = re.sub(r'<[^>]+>', '', self.content or '')
        words = len(text.split())
        return max(1, round(words / 200))
