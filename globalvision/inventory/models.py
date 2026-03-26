from django.db import models

class Vehicle(models.Model):
    CATEGORY_CHOICES = [
        ('Car', 'Car'),
        ('Jeep', 'Jeep'),
        ('Motorbike', 'Motorbike'),
        ('Bicycle', 'Bicycle'),
    ]
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Rented', 'Rented'),
        ('Maintenance', 'Maintenance'),
    ]
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Car')
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    image = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'dashboard_vehicle'

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

    class Meta:
        db_table = 'dashboard_equipment'

    def save(self, *args, **kwargs):
        if self.stock <= 0:
            self.status = 'Out of Stock'
        elif self.status == 'Out of Stock' and self.stock > 0:
            self.status = 'Available'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
