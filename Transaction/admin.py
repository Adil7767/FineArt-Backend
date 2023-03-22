from django.contrib import admin
from Transaction.models import *


# Create your models here.
class TypeAdmin(admin.ModelAdmin):
    list_display = ['add_type']


class PaymentsAdmin(admin.ModelAdmin):
    list_display = ['icons', 'payment_method']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['new_category', 'icons', 'color']


class Add_TransactionAdmin(admin.ModelAdmin):
    list_display = ['type', 'payment_method', 'description', 'category', 'amount', 'image', 'created_at', 'updated_at', 'frequency']
    # list_filter = ('user',)
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Transaction info', {'fields': ('type', 'payment_method', 'category', 'image', 'frequency')}),
        ('Amount', {'fields': ('amount',)}),
        ('Description', {'fields': ('description',)}),

    )


admin.site.register(Type, TypeAdmin)
admin.site.register(Payment, PaymentsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Add_Transaction, Add_TransactionAdmin)