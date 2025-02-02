from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import datetime
from cryptography.fernet import Fernet
from django.conf import settings

card_number_validator = RegexValidator(
    regex=r'^\d{13,19}$',
    message="رقم البطاقة يجب أن يكون بين 13 و 19 رقمًا."
)

def luhn_check(card_number: str) -> bool:
    """التحقق من صحة رقم البطاقة باستخدام خوارزمية Luhn"""
    card_number = card_number.replace(" ", "")
    if not card_number.isdigit():
        return False

    total = 0
    reverse_digits = list(map(int, card_number[::-1]))

    for i, digit in enumerate(reverse_digits):
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit

    return total % 10 == 0

class CreditCard(models.Model):
    """نموذج لحفظ بيانات بطاقات الائتمان بتشفير الرقم"""
    
    encrypted_card_number = models.BinaryField(default=b'')

    expiry_month = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name="شهر الانتهاء"
    )

    expiry_year = models.IntegerField(
        validators=[MinValueValidator(datetime.datetime.now().year)],
        verbose_name="سنة الانتهاء"
    )

    security_code = models.CharField(
        max_length=4,
        validators=[RegexValidator(regex=r'^\d{3,4}$', message="يجب أن يكون رمز الأمان مكونًا من 3 أو 4 أرقام.")],
        verbose_name="رمز الأمان"
    )

    card_holder_name = models.CharField(max_length=255, verbose_name="اسم حامل البطاقة")

    def clean(self):
        """التحقق من صحة البطاقة قبل الحفظ"""
        if not luhn_check(self.get_card_number()):
            raise ValidationError({"card_number": "رقم البطاقة غير صالح وفقًا لخوارزمية Luhn."})
    
        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month
        if self.expiry_year < current_year or (self.expiry_year == current_year and self.expiry_month < current_month):
            raise ValidationError({"expiry_year": "البطاقة منتهية الصلاحية."})

    def is_expired(self):
        """التحقق مما إذا كانت البطاقة منتهية الصلاحية"""
        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month
        return (self.expiry_year < current_year) or (self.expiry_year == current_year and self.expiry_month < current_month)

    def set_card_number(self, card_number):
        """تشفير رقم البطاقة قبل الحفظ"""
        f = settings.FERNET
        encrypted_data = f.encrypt(card_number.encode())
        self.encrypted_card_number = encrypted_data

    def get_card_number(self):
        """فك تشفير رقم البطاقة عند الحاجة"""
        f = settings.FERNET
        return f.decrypt(self.encrypted_card_number).decode()

    def __str__(self):
        return f"بطاقة **** {self.get_card_number()[-4:]} الخاصة بـ {self.card_holder_name}"
    