from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"

    def ready(self):
        from django.contrib.auth import get_user_model

        def create_default_admin(sender, **kwargs):
            if sender.name != self.name:
                return
            User = get_user_model()
            if not User.objects.filter(mobile_number='9730707765').exists():
                User.objects.create_superuser(
                    mobile_number='9730707765',
                    password='user@1234',
                    role=User.ADMIN,
                )

        post_migrate.connect(create_default_admin, sender=self)
