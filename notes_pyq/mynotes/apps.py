from django.apps import AppConfig


class MynotesConfig(AppConfig):
    name = 'mynotes'

    def ready(self):
        import mynotes.signals