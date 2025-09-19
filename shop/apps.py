# App configuration for the 'shop' Django app.
# This class is used by Django to set up app-specific configurations.

from django.apps import AppConfig

class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'
