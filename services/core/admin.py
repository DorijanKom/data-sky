from django.contrib import admin
from django.apps import apps

for model_class in apps.get_app_config("core").get_models():
    if not admin.site.is_registered(model_class):
        admin.site.register(model_class)
