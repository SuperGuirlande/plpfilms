from django.contrib import admin
from django.utils.html import format_html

from .models import PortfolioCategory, PortfolioEntry, PortfolioVideo


# ─────────────────────────────────────────────
#  Catégorie
# ─────────────────────────────────────────────

@admin.register(PortfolioCategory)
class PortfolioCategoryAdmin(admin.ModelAdmin):
    list_display  = ['name', 'slug', 'entry_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

    def entry_count(self, obj):
        count = obj.entries.count()
        return format_html('<b>{}</b>', count)
    entry_count.short_description = "Entrées"


# ─────────────────────────────────────────────
#  Vidéo (inline dans PortfolioEntry)
# ─────────────────────────────────────────────

class PortfolioVideoInline(admin.TabularInline):
    model  = PortfolioVideo
    extra  = 1
    fields = ['title', 'video_type', 'youtube_url', 'file', 'order']
    verbose_name        = "Vidéo"
    verbose_name_plural = "Vidéos associées"


# ─────────────────────────────────────────────
#  Entrée portfolio
# ─────────────────────────────────────────────

@admin.register(PortfolioEntry)
class PortfolioEntryAdmin(admin.ModelAdmin):

    # Liste
    list_display       = ['thumbnail_preview', 'title', 'category', 'is_published', 'created_at']
    list_display_links = ['thumbnail_preview', 'title']
    list_editable      = ['is_published']
    list_filter        = ['category', 'is_published', 'created_at']
    search_fields      = ['title', 'short_description']
    date_hierarchy     = 'created_at'

    # Formulaire
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PortfolioVideoInline]

    fieldsets = (
        ('Informations principales', {
            'fields': ('title', 'slug', 'category', 'is_published'),
        }),
        ('Médias', {
            'fields': ('thumbnail', 'short_description'),
        }),
        ('Contenu de la page', {
            'description': 'Rédigez ici le détail complet de l\'entrée (contexte, processus, résultats…)',
            'fields': ('content',),
            'classes': ('wide',),
        }),
    )

    # Colonne aperçu miniature
    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="height:48px;width:72px;object-fit:cover;border-radius:4px;" />',
                obj.thumbnail.url,
            )
        return "—"
    thumbnail_preview.short_description = "Aperçu"
