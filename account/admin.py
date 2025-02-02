from django.contrib import admin
from .models import CreditCard

@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    list_display = ("card_holder_name", "masked_card_number", "expiry_month", "expiry_year", "is_expired_display")

    def masked_card_number(self, obj):
        return f"**** **** **** {obj.get_card_number()[-4:]}"

    masked_card_number.short_description = "رقم البطاقة"

    def is_expired_display(self, obj):
        return "نعم" if obj.is_expired() else "لا"

    is_expired_display.boolean = True
    is_expired_display.short_description = "منتهية؟"
