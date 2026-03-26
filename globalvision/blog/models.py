from django.db import models
from django.conf import settings
from django.utils.text import slugify

class BlogPost(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('accepted', 'Accepted & Published'),
        ('rejected', 'Rejected'),
    )

    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True, default='')
    body = models.TextField(default='')
    cover_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    category = models.CharField(max_length=100, default='General')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='blog_posts')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    rejection_reason = models.TextField(blank=True, null=True)
    admin_note = models.TextField(blank=True, null=True)
    
    is_published = models.BooleanField(default=False)  # Redundant with status='accepted', but good for compatibility
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dashboard_blogpost'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Sync is_published with status
        self.is_published = (self.status == 'accepted')
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def word_count(self):
        return len(self.body.split())

    @property
    def read_time(self):
        return max(1, round(self.word_count / 200))
