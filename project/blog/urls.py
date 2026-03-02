from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # ── Admin ──────────────────────────────────
    # Articles
    path('articles/',                      views.admin_post_list,      name='admin_post_list'),
    path('articles/nouveau/',              views.admin_post_create,    name='admin_post_create'),
    path('articles/<int:pk>/modifier/',    views.admin_post_edit,      name='admin_post_edit'),
    path('articles/<int:pk>/supprimer/',   views.admin_post_delete,    name='admin_post_delete'),
    # Catégories
    path('categories/',                    views.admin_category_list,   name='admin_category_list'),
    path('categories/nouvelle/',           views.admin_category_create, name='admin_category_create'),
    path('categories/<int:pk>/modifier/',  views.admin_category_edit,   name='admin_category_edit'),
    path('categories/<int:pk>/supprimer/', views.admin_category_delete, name='admin_category_delete'),
    # Tags
    path('tags/',                          views.admin_tag_list,   name='admin_tag_list'),
    path('tags/nouveau/',                  views.admin_tag_create, name='admin_tag_create'),
    path('tags/<int:pk>/supprimer/',       views.admin_tag_delete, name='admin_tag_delete'),
]
