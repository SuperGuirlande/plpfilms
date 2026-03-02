from django.contrib import admin
from django.utils.html import format_html
from .models import BlogCategory, BlogTag, BlogPost


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display        = ['name', 'slug', 'post_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields       = ['name']

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = "Articles"


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display        = ['name', 'slug', 'post_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields       = ['name']

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = "Articles"


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display        = ['cover_preview', 'title', 'category', 'status', 'is_featured', 'published_at']
    list_display_links  = ['cover_preview', 'title']
    list_editable       = ['status', 'is_featured']
    list_filter         = ['status', 'is_featured', 'category', 'published_at']
    search_fields       = ['title', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal   = ['tags']
    date_hierarchy      = 'published_at'

    fieldsets = (
        ('Contenu', {
            'fields': ('title', 'slug', 'category', 'tags', 'author', 'cover', 'excerpt', 'content'),
        }),
        ('Publication', {
            'fields': ('status', 'is_featured', 'published_at'),
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
        }),
    )

    def cover_preview(self, obj):
        if obj.cover:
            return format_html(
                '<img src="{}" style="height:48px;width:72px;object-fit:cover;border-radius:4px;" />',
                obj.cover.url,
            )
        return "—"
    cover_preview.short_description = "Couverture"
