from django.db import models
from user_control.models import CustomUser
from io import BytesIO
from django.core.files import File
from datetime import datetime
from random import randint

import qrcode
# import barcode
# from barcode.writer import ImageWriter
# from PIL import Image, ImageDraw



BUNDLE_CHOICES = (
    ("Home", "Home"), ("Classic", "Classic"), ("Premium", "Premium"), 
)

BUNDLE_DURATION_TYPE_CHOICES = (
    ("Days", "Days"), ("Months", "Months"), 
)


class Customer(models.Model):
    first_name = models.CharField(max_length=50, blank=False, unique=False)
    last_name = models.CharField(max_length=50, blank=False, unique=False)
    address = models.CharField(max_length=50, blank=False, unique=False)
    telephone_one = models.CharField(max_length=50, blank=False, unique=True)
    telephone_two = models.CharField(max_length=50, blank=True, null=True, unique=False)
    email = models.EmailField(max_length=50, blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, null=True, related_name='customer_created_by', on_delete=models.SET_NULL)
    created_at = models.DateField(auto_now_add=True)
    updated_by = models.ForeignKey(CustomUser, null=True, related_name='customer_updated_by', on_delete=models.SET_NULL)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        constraints = [ 
            models.UniqueConstraint(fields=["telephone_one"], name="customer_unique"),
            models.UniqueConstraint(fields=["first_name", "last_name"], name="firstname_last_name"),
        ]

    def __str__(self):
        return f"{self.first_name}"
    

class Bundle(models.Model):
    bundle_name = models.CharField(max_length=50, blank=False, unique=True)
    bundle_price = models.CharField(max_length=50, blank=False, null=False)
    bundle_data = models.CharField(max_length=6, blank=False, null=False)
    bundle_data_type = models.CharField(max_length=3, blank=False, null=False)
    bundle_duration = models.CharField(max_length=50, blank=False, null=False)
    bundle_duration_type = models.CharField(max_length=15, choices=BUNDLE_DURATION_TYPE_CHOICES, blank=False)
    bundle_type = models.CharField(max_length=15, choices=BUNDLE_CHOICES, blank=False)
    bundle_limitted = models.BooleanField(default=True, blank=False)
    created_by = models.ForeignKey(CustomUser, null=True, related_name='bundle_created_by', on_delete=models.SET_NULL)
    created_at = models.DateField(auto_now_add=True)
    updated_by = models.ForeignKey(CustomUser, null=True, related_name='bundle_updated_by', on_delete=models.SET_NULL)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        constraints = [ 
            models.UniqueConstraint(fields=["bundle_data", "bundle_duration", "bundle_limitted"], name="data_duration_limitted")
        ]

    def __str__(self):
        return f"{self.id} {self.bundle_name}"


class Transactions(models.Model):
    code = models.CharField(max_length=7, null=True, blank=True, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    details = models.CharField(max_length=100, blank=True, null=True)
    bundle = models.ForeignKey(Bundle, null=True, related_name='transactions_bundle', on_delete=models.SET_NULL)
    barcode = models.ImageField(upload_to='images/', blank=True)
    qrcode = models.ImageField(upload_to='images/', blank=True)
    alt_text = models.CharField(max_length=50, null=True, blank=True)
    details = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(CustomUser, null=True, related_name='transactions_created_by', on_delete=models.SET_NULL)
    created_at = models.DateField(auto_now_add=True)
    updated_by = models.ForeignKey(CustomUser, null=True, related_name='transactions_updated_by', on_delete=models.SET_NULL)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.code}"

    # def save(self, *args, **kwargs):
    #     EAN = barcode.get_barcode_class("ean13")
    #     print(EAN)
    #     ean = EAN("103456789012", writer=ImageWriter())
    #     print(ean)
    #     buffer = BytesIO()
    #     print(buffer)
    #     ean.write(buffer)
    #     self.barcode.save("barcode.png", File(buffer), save=False)
    #     return super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make( 
            self.customer.first_name + " " + 
            self.customer.last_name + " - " + 
            self.bundle.bundle_name + " " + 
            self.bundle.bundle_price + "F " + 
            str(self.bundle.bundle_data) + 
            str(self.bundle.bundle_data_type)
        )
        canvas = Image.new("RGB", (350, 350), "white")
        # draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f"qrcode-{self.customer.first_name + self.customer.last_name}" + ".png"
        buffer = BytesIO()
        canvas.save(buffer, "PNG")
        date = str(datetime.now())
        self.alt_text = f"{self.customer.first_name}" + "_picture"
        int = date[2: 4] + str(randint(100, 999)) + date[5: 7]
        self.code = int
        self.qrcode.save(fname, File(buffer), save=False)
        canvas.close()
        return super().save(*args, **kwargs)
