from django.apps import AppConfig


###############################################################################
###############################################################################
class CoreServiceConfig(AppConfig):
    label = "core"
    verbose_name = "Core"
    name = "services.core"

    def ready(self):
        import services.core.signals
