from django.db import models

class AboutPage(models.Model):
    mission = models.TextField(default='')
    story = models.TextField(default='')
    stat_years = models.IntegerField(default=0, verbose_name="Years of Experience")
    stat_treks = models.IntegerField(default=0, verbose_name="Treks Completed")
    stat_clients = models.IntegerField(default=0, verbose_name="Happy Clients")
    stat_team = models.IntegerField(default=0, verbose_name="Team Members")
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return "About Us Content"

class TeamMember(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    favourite_trek = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.name

class SiteSettings(models.Model):
    phone = models.CharField(max_length=20, blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    maps_embed = models.TextField(blank=True)
    hours = models.CharField(max_length=200, blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    tripadvisor_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Site Settings"
