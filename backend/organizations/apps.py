from django.apps import AppConfig


class OrganizationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'organizations'
    
    def ready(self):
        try:
            import organizations.signals
        except Exception as e:
            print(f"Error importing organizations signals: {e}")