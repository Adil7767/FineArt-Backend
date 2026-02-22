import json
from django.db import models
from colorfield.fields import ColorField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from account.models import User

# Optional: avoid importing django_celery_beat at module load so runserver can start
# even when Celery has import issues (e.g. current_app on some Python/Celery versions).
try:
    from django_celery_beat.models import PeriodicTask, CrontabSchedule
    _CELERY_BEAT_AVAILABLE = True
except Exception:
    PeriodicTask = None
    CrontabSchedule = None
    _CELERY_BEAT_AVAILABLE = False


class Type(models.Model):
    add_type = models.CharField(max_length=255)

    def __str__(self):
        return self.add_type


class Payment(models.Model):
    icons = models.ImageField(upload_to='payment-icons/%Y/%m/%d/', null=True, blank=True)
    payment_method = models.CharField(max_length=255)

    def __str__(self):
        return self.payment_method


class Category(models.Model):
    new_category = models.CharField(max_length=255)
    icons = models.ImageField(upload_to='category-icons/%Y/%m/%d/', null=True, blank=True)
    color = ColorField(format="hexa", image_field="icons")

    def __str__(self):
        return self.new_category


class Add_Transaction(models.Model):
    NON_RECURRING = 'none'
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    EVERY_THREE_MONTHS = 'every_three_months'
    EVERY_SIX_MONTHS = 'every_six_months'
    YEARLY = 'yearly'

    FREQUENCY_CHOICES = [
        (NON_RECURRING, 'Non-recurring'),
        (DAILY, 'daily'),
        (WEEKLY, 'weekly'),
        (MONTHLY, 'monthly'),
        (EVERY_THREE_MONTHS, 'every_three_months'),
        (EVERY_SIX_MONTHS, 'every_six_months'),
        (YEARLY, 'yearly')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='types')
    payment_method = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='payment')
    description = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='record-icons/%Y/%m/%d/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)


@receiver(post_save, sender=Add_Transaction)
def regenerate_trans(sender, instance, created, **kwargs):
    if not _CELERY_BEAT_AVAILABLE or not created:
        return
    if instance.frequency == 'daily':
        schedule, created = CrontabSchedule.objects.get_or_create(hour=instance.created_at.hour,
                                                                  minute=instance.created_at.minute)
        task = PeriodicTask.objects.create(crontab=schedule,
                                           name="daily-regenerate-existing-data-" + str(instance.id),
                                           task="Transaction.tasks.regenerate_transaction",
                                           args=json.dumps((instance.id,)))
    elif instance.frequency == 'weekly':
        transaction_date = timezone.now().date().weekday()
        schedule, created = CrontabSchedule.objects.get_or_create(hour=instance.created_at.hour+5,
                                                                  minute=instance.created_at.minute,
                                                                  day_of_week=transaction_date)
        task = PeriodicTask.objects.create(crontab=schedule,
                                           name="daily-regenerate-existing-data-" + str(instance.id),
                                           task="Transaction.tasks.regenerate_transaction",
                                           args=json.dumps((instance.id,)))
    elif instance.frequency == 'monthly':
        transaction_date = timezone.now().date().day
        schedule, created = CrontabSchedule.objects.get_or_create(hour=instance.created_at.hour+5,
                                                                  minute=instance.created_at.minute,
                                                                  day_of_month=transaction_date)
        task = PeriodicTask.objects.create(crontab=schedule,
                                           name="daily-regenerate-existing-data-" + str(instance.id),
                                           task="Transaction.tasks.regenerate_transaction",
                                           args=json.dumps((instance.id,)))
    elif instance.frequency == 'every_three_months':
        schedule, created = CrontabSchedule.objects.get_or_create(hour=instance.created_at.hour+5,
                                                                  minute=instance.created_at.minute,
                                                                  day_of_month="*/3")
        task = PeriodicTask.objects.create(crontab=schedule,
                                           name="daily-regenerate-existing-data-" + str(instance.id),
                                           task="Transaction.tasks.regenerate_transaction",
                                           args=json.dumps((instance.id,)))
    elif instance.frequency == 'every_six_months':
        schedule, created = CrontabSchedule.objects.get_or_create(hour=instance.created_at.hour+5,
                                                                  minute=instance.created_at.minute,
                                                                  day_of_month="*/6")
        task = PeriodicTask.objects.create(crontab=schedule,
                                           name="daily-regenerate-existing-data-" + str(instance.id),
                                           task="Transaction.tasks.regenerate_transaction",
                                           args=json.dumps((instance.id,)))
    elif instance.frequency == 'yearly':
        transaction_date = timezone.now().date().month
        date = timezone.now().date().day
        schedule, created = CrontabSchedule.objects.get_or_create(hour=instance.created_at.hour+5,
                                                                  minute=instance.created_at.minute,
                                                                  month_of_year=transaction_date,
                                                                  day_of_month=date)
        task = PeriodicTask.objects.create(crontab=schedule,
                                           name="daily-regenerate-existing-data-" + str(instance.id),
                                           task="Transaction.tasks.regenerate_transaction",
                                           args=json.dumps((instance.id,)))
