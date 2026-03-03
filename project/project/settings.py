from pathlib import Path
import environ
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ENVIRON #
env = environ.Env()
environ.Env.read_env(env_file=str(BASE_DIR / 'project' / '.env'))

SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'tailwind',
    'django_ckeditor_5',
    'theme',

    'accounts',
    'main',
    'portfolio',
    'blog',
    # 'contact_management',
    # 'blog',
    # 'shop',

    # 'contact_management',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'project/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'accounts.context_processor.get_active_links',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': env('DB_NAME'),
            'USER': env('DB_USER'),
            'PASSWORD': env('DB_PASSWORD'),
            'HOST': env('DB_HOST'),
            'PORT': env('DB_PORT'),
        }   
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# TIMEZONE
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

# STATIC & MEDIA #
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
    BASE_DIR / 'main' / 'static',
    # BASE_DIR / 'accounts' / 'static',
    # BASE_DIR / 'blog' / 'static',
    # BASE_DIR / 'shop' / 'static',
    # BASE_DIR / 'ckeditor_config' / 'static',
    ]
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# TAILWIND #
NPM_BIN_PATH = 'C:/Program Files/nodejs/npm.cmd'
TAILWIND_APP_NAME = 'theme'

# USER MODEL #
AUTH_USER_MODEL = 'accounts.CustomUser'

# LOGIN
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'accounts:my_account'

# EMAIL SETTINGS #
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('SMTP_HOST')
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = env('SMTP_PASS')
DEFAULT_FROM_EMAIL = 'contact@agencecodemaster.com'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CKEDITOR 5 — upload des images dans l'éditeur
CKEDITOR_5_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
CKEDITOR_5_UPLOAD_FILE_TYPES = ['jpeg', 'jpg', 'png', 'gif', 'webp']




# ─────────────────────────────────────────────────────────────
# CKEDITOR 5 — Configuration PLP Films
# ─────────────────────────────────────────────────────────────

# Palette de couleurs du site
PLP_COLORS = [
    # Fonds
    { 'color': '#0A0A0A', 'label': 'Noir Profond'  },
    { 'color': '#1A1A1A', 'label': 'Noir Doux'     },
    { 'color': '#2A2A2A', 'label': 'Gris Foncé'    },
    # Or
    { 'color': '#D4AF37', 'label': 'Or'             },
    { 'color': '#E6C96E', 'label': 'Or Clair'       },
    { 'color': '#B8960C', 'label': 'Or Foncé'       },
    # Blancs
    { 'color': '#F5F5F5', 'label': 'Blanc Cassé'   },
    { 'color': '#FFFFFF', 'label': 'Blanc Pur'      },
    { 'color': '#CCCCCC', 'label': 'Gris Clair'     },
    # Couleurs fonctionnelles
    { 'color': '#ef4444', 'label': 'Rouge'          },
    { 'color': '#22c55e', 'label': 'Vert'           },
    { 'color': '#3b82f6', 'label': 'Bleu'           },
]

CKEDITOR_5_CONFIGS = {

    # ── Config légère (champs simples) ──────────────────────────
    'default': {
        'language'   : 'fr',
        'contentsCss': ['/static/css/plp_content.css'],
        'toolbar': {
            'items': [
                'heading', '|',
                'bold', 'italic', 'link', '|',
                'bulletedList', 'numberedList', 'blockQuote',
            ],
        },
        'heading': {
            'options': [
                { 'model': 'paragraph',  'title': 'Paragraphe',  'class': 'ck-heading_paragraph'  },
                { 'model': 'heading1', 'view': 'h2', 'title': 'Titre (Bebas Neue)',     'class': 'ck-heading_heading2' },
                { 'model': 'heading2', 'view': 'h3', 'title': 'Sous-titre (Oswald)',    'class': 'ck-heading_heading3' },
                { 'model': 'heading3', 'view': 'h4', 'title': 'Sous-titre 2 (Oswald)', 'class': 'ck-heading_heading4' },
            ]
        },
    },

    # ── Config complète (portfolio, blog) ───────────────────────
    'blog': {
        'language'   : 'fr',
        'contentsCss': ['/static/css/plp_content.css'],

        'toolbar': {
            'shouldNotGroupWhenFull': True,
            'items': [
                # Typographie
                'heading', 'fontFamily', 'fontSize', '|',
                # Mise en forme
                'bold', 'italic', 'underline', 'strikethrough', '|',
                # Couleurs
                'fontColor', 'fontBackgroundColor', 'highlight', '|',
                # Alignement
                'alignment', 'outdent', 'indent', '|',
                # Listes & blocs
                'bulletedList', 'numberedList', 'todoList', 'blockQuote', '|',
                # Médias
                'insertImage', 'mediaEmbed', 'insertTable', '|',
                # Code & avancé
                'link', 'code', 'codeBlock', 'sourceEditing', 'removeFormat',
            ],
        },

        # Titres avec labels clairs pour Pierrick
        'heading': {
            'options': [
                { 'model': 'paragraph',  'title': 'Paragraphe — Inter',           'class': 'ck-heading_paragraph'  },
                { 'model': 'heading1', 'view': 'h2', 'title': 'Titre — Bebas Neue',       'class': 'ck-heading_heading2' },
                { 'model': 'heading2', 'view': 'h3', 'title': 'Sous-titre — Oswald Or',   'class': 'ck-heading_heading3' },
                { 'model': 'heading3', 'view': 'h4', 'title': 'Sous-titre 2 — Oswald',    'class': 'ck-heading_heading4' },
            ]
        },

        # Polices du site
        'fontFamily': {
            'options': [
                'default',
                'Inter, sans-serif',
                'Oswald, sans-serif',
                "'Bebas Neue', sans-serif",
                "'Courier New', Courier, monospace",
            ],
            'supportAllValues': True,
        },

        # Tailles cohérentes avec le CSS du site
        'fontSize': {
            'options': [
                { 'title': 'Petit — 0.85rem',    'model': '0.85rem'  },
                { 'title': 'Normal — 1rem',       'model': '1rem'     },
                { 'title': 'Moyen — 1.1rem',      'model': '1.1rem'   },
                { 'title': 'Grand — 1.4rem',      'model': '1.4rem'   },
                { 'title': 'H3 — 1.8rem',         'model': '1.8rem'   },
                { 'title': 'H2 — 3.5rem',         'model': '3.5rem'   },
            ],
            'supportAllValues': True,
        },

        # Couleurs texte — palette PLP
        'fontColor': {
            'colors': PLP_COLORS,
            'columns': 3,
        },

        # Couleurs fond texte — palette PLP
        'fontBackgroundColor': {
            'colors': PLP_COLORS,
            'columns': 3,
        },

        # Surligneurs adaptés au thème sombre
        'highlight': {
            'options': [
                {
                    'model': 'orMarker',
                    'class': 'marker-or',
                    'title': 'Surligneur Or',
                    'color': 'rgba(212,175,55,0.35)',
                    'type' : 'marker',
                },
                {
                    'model': 'orFondMarker',
                    'class': 'marker-or-fond',
                    'title': 'Fond Or foncé',
                    'color': 'rgba(212,175,55,0.12)',
                    'type' : 'marker',
                },
                {
                    'model': 'grisMarker',
                    'class': 'marker-gris',
                    'title': 'Fond Gris Foncé',
                    'color': '#2A2A2A',
                    'type' : 'marker',
                },
                {
                    'model': 'rougeMarker',
                    'class': 'marker-rouge',
                    'title': 'Surligneur Rouge',
                    'color': 'rgba(239,68,68,0.3)',
                    'type' : 'marker',
                },
                {
                    'model': 'blancPen',
                    'class': 'pen-blanc',
                    'title': 'Texte Blanc',
                    'color': '#FFFFFF',
                    'type' : 'pen',
                },
                {
                    'model': 'orPen',
                    'class': 'pen-or',
                    'title': 'Texte Or',
                    'color': '#D4AF37',
                    'type' : 'pen',
                },
            ]
        },

        # Images
        'image': {
            'toolbar': [
                'imageTextAlternative', '|',
                'imageStyle:alignLeft', 'imageStyle:alignCenter', 'imageStyle:alignRight',
            ],
            'styles': ['full', 'alignLeft', 'alignRight', 'alignCenter'],
        },

        # Tableaux avec palette PLP
        'table': {
            'contentToolbar': [
                'tableColumn', 'tableRow', 'mergeTableCells',
                'tableProperties', 'tableCellProperties',
            ],
            'tableProperties': {
                'borderColors'    : PLP_COLORS,
                'backgroundColors': PLP_COLORS,
            },
            'tableCellProperties': {
                'borderColors'    : PLP_COLORS,
                'backgroundColors': PLP_COLORS,
            },
        },

        # Listes
        'list': {
            'properties': {
                'styles'    : True,
                'startIndex': True,
                'reversed'  : True,
            }
        },

        # HTML étendu (h4 autorisé)
        'htmlSupport': {
            'allow': [
                { 'name': 'h4', 'attributes': True, 'classes': True, 'styles': True },
            ]
        },
    },
}