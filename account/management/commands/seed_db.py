"""
Seed database with a test user and optional types/categories/payments.
Run: python manage.py seed_db
Creates user: dev.adil786@gmail.com / AdArtDemo123!
"""
from django.core.management.base import BaseCommand
from django.db import connection
from account.models import User
from Transaction.models import Type, Category, Payment, Add_Transaction


# Default test user (matches APP_CONFIG contact email)
SEED_EMAIL = "dev.adil786@gmail.com"
SEED_PASSWORD = "AdArtDemo123!"
SEED_FIRST_NAME = "Adil"
SEED_LAST_NAME = "Mustafa"
SEED_GENDER = "M"
SEED_PHONE = "12345678901"


class Command(BaseCommand):
    help = "Create database tables (migrate), seed test user and optional types/categories/payments."

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-migrate",
            action="store_true",
            help="Do not run migrations (only seed data).",
        )

    def handle(self, *args, **options):
        if not options["no_migrate"]:
            self.stdout.write("Running migrations...")
            from django.core.management import call_command
            call_command("migrate", verbosity=1)
            self.stdout.write(self.style.SUCCESS("Migrations done."))

        # Seed user
        if User.objects.filter(email=SEED_EMAIL).exists():
            self.stdout.write(f"User {SEED_EMAIL} already exists.")
            user = User.objects.get(email=SEED_EMAIL)
        else:
            user = User.objects.create_user(
                email=SEED_EMAIL,
                first_name=SEED_FIRST_NAME,
                last_name=SEED_LAST_NAME,
                gender=SEED_GENDER,
                phone_number=SEED_PHONE,
                password=SEED_PASSWORD,
            )
            self.stdout.write(self.style.SUCCESS(f"Created user: {SEED_EMAIL}"))

        # Seed types if empty
        if Type.objects.count() == 0:
            for name in ["Income", "Expense", "Transfer", "Bill", "Investment"]:
                Type.objects.create(add_type=name)
            self.stdout.write(self.style.SUCCESS("Created types."))

        # Seed categories if empty (color required by ColorField)
        if Category.objects.count() == 0:
            for name in ["Food", "Transport", "Shopping", "Utilities", "Health", "Other"]:
                Category.objects.create(new_category=name, color="#5B39CB")
            self.stdout.write(self.style.SUCCESS("Created categories."))

        # Seed payments if empty
        if Payment.objects.count() == 0:
            for name in ["Cash", "Card", "Bank Transfer", "UPI"]:
                Payment.objects.create(payment_method=name)
            self.stdout.write(self.style.SUCCESS("Created payment methods."))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("=== Login credentials (AdArt app) ==="))
        self.stdout.write(f"  Email:    {SEED_EMAIL}")
        self.stdout.write(f"  Password: {SEED_PASSWORD}")
        self.stdout.write("")
