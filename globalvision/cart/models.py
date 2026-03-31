from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'account_cart'

    def __str__(self):
        return f"Cart for {self.user.user_name}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default=1)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    @property
    def days(self):
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            return max(delta.days, 1)
        return 1

    class Meta:
        db_table = 'account_cartitem'

    def __str__(self):
        if self.content_object:
            return f"{self.quantity} x {self.content_object}"
        return f"{self.quantity} x Unknown Product"

    @property
    def total_price(self):
        if self.content_object:
            return self.content_object.price_per_day * self.days * self.quantity
        return 0
