import re
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class PortfolioCategory(models.Model):
    """Type de projet : Court-métrage, Clip musical, Captation, Publicité..."""

    name = models.CharField(max_length=100, verbose_name="Nom")
    slug = models.SlugField(unique=True, verbose_name="Slug")

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['name']

    def __str__(self):
        return self.name


class PortfolioEntry(models.Model):
    """Entrée au portfolio — étude de cas complète."""

    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    category = models.ForeignKey(
        PortfolioCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='entries',
        verbose_name="Catégorie",
    )
    thumbnail = models.ImageField(
        upload_to='portfolio/thumbnails/',
        verbose_name="Miniature",
    )
    short_description = models.CharField(
        max_length=300,
        verbose_name="Description courte",
        help_text="Affiché dans la grille portfolio (max 300 caractères).",
    )
    content = CKEditor5Field(
        verbose_name="Contenu de la page",
        config_name='blog',
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="Publié",
        help_text="Décocher pour masquer du site sans supprimer.",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")

    class Meta:
        verbose_name = "Entrée portfolio"
        verbose_name_plural = "Entrées portfolio"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class PortfolioVideo(models.Model):
    """Vidéo liée à une entrée — fichier direct ou lien YouTube."""

    VIDEO_TYPE_CHOICES = [
        ('youtube', 'Lien YouTube'),
        ('file', 'Fichier vidéo'),
    ]

    entry = models.ForeignKey(
        PortfolioEntry,
        on_delete=models.CASCADE,
        related_name='videos',
        verbose_name="Entrée portfolio",
    )
    title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Titre de la vidéo",
    )
    video_type = models.CharField(
        max_length=10,
        choices=VIDEO_TYPE_CHOICES,
        default='youtube',
        verbose_name="Type",
    )
    youtube_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="URL YouTube",
        help_text="Ex : https://www.youtube.com/watch?v=XXXX ou https://youtu.be/XXXX",
    )
    file = models.FileField(
        upload_to='portfolio/videos/',
        blank=True,
        null=True,
        verbose_name="Fichier vidéo",
        help_text="Formats acceptés : mp4, mov, webm.",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")

    class Meta:
        verbose_name = "Vidéo"
        verbose_name_plural = "Vidéos"
        ordering = ['order']

    def __str__(self):
        label = self.title or "Vidéo"
        return f"{label} — {self.entry.title}"

    @property
    def video_id(self):
        """Extrait l'identifiant YouTube (11 caractères)."""
        if self.video_type == 'youtube' and self.youtube_url:
            match = re.search(
                r'(?:v=|youtu\.be/|embed/)([a-zA-Z0-9_-]{11})',
                self.youtube_url,
            )
            if match:
                return match.group(1)
        return None

    @property
    def embed_url(self):
        """URL d'embed YouTube avec paramètres optimisés."""
        vid = self.video_id
        if vid:
            return f"https://www.youtube.com/embed/{vid}?rel=0&modestbranding=1&autoplay=1"
        return None

    @property
    def thumbnail_url(self):
        """Miniature haute résolution de la vidéo YouTube."""
        vid = self.video_id
        if vid:
            return f"https://img.youtube.com/vi/{vid}/maxresdefault.jpg"
        return None
