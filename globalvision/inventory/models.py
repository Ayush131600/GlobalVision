from django.db import models

class Vehicle(models.Model):
    CATEGORY_CHOICES = [
        ('Luxury', 'Luxury'),
        ('Off Road', 'Off Road'),
        ('Vans', 'Vans'),
    ]
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Rented', 'Rented'),
        ('Maintenance', 'Maintenance'),
    ]
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Luxury')
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    stock = models.IntegerField(default=1)
    image = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.stock <= 0:
            self.status = 'Rented' if self.status == 'Rented' else 'Maintenance' if self.status == 'Maintenance' else 'Rented'
            # Actually, if stock is 0, it should probably be 'Rented' or 'Not Available'.
            # The current status choices are 'Available', 'Rented', 'Maintenance'.
            # If stock is 0, we can set it to 'Rented' (as in all units are rented).
            if self.status == 'Available':
                self.status = 'Rented'
        elif self.status == 'Rented' and self.stock > 0:
            self.status = 'Available'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Equipment(models.Model):
    CATEGORY_CHOICES = [
        ('Trekking', 'Trekking'),
        ('Camping', 'Camping'),
        ('Climbing', 'Climbing'),
        ('Safety', 'Safety'),
    ]
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Out of Stock', 'Out of Stock'),
    ]
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Trekking')
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    image = models.ImageField(upload_to='equipment/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if self.stock <= 0:
            self.status = 'Out of Stock'
        elif self.status == 'Out of Stock' and self.stock > 0:
            self.status = 'Available'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
