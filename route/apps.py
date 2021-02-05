from django.apps import AppConfig


class RouteConfig(AppConfig):
    name = 'route'

    def ready(self):
        import route.signals