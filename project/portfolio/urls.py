from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    # Catégories
    path('categories/',                      views.admin_category_list,   name='admin_category_list'),
    path('categories/nouvelle/',             views.admin_category_create, name='admin_category_create'),
    path('categories/<int:pk>/modifier/',    views.admin_category_edit,   name='admin_category_edit'),
    path('categories/<int:pk>/supprimer/',   views.admin_category_delete, name='admin_category_delete'),

    # Entrées
    path('entrees/',                         views.admin_entry_list,   name='admin_entry_list'),
    path('entrees/nouvelle/',                views.admin_entry_create, name='admin_entry_create'),
    path('entrees/<int:pk>/modifier/',       views.admin_entry_edit,   name='admin_entry_edit'),
    path('entrees/<int:pk>/supprimer/',      views.admin_entry_delete, name='admin_entry_delete'),
]
