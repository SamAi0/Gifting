from django.db import models

class Testimonial(models.Model):
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    message = models.TextField()
    
    def __str__(self):
        return f"Testimonial by {self.name}"

class Settings(models.Model):
    company_name = models.CharField(max_length=200, default="Soham Gift")
    tagline = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    address = models.TextField()
    phone1 = models.CharField(max_length=20)
    phone2 = models.CharField(max_length=20, blank=True)
    email = models.EmailField()
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    
    class Meta:
        verbose_name = "Business Information"
        verbose_name_plural = "Business Information"
    
    def __str__(self):
        return self.company_name
    
    def save(self, *args, **kwargs):
        # Ensure only one instance of Settings exists
        if not self.pk and Settings.objects.exists():
            return
        return super().save(*args, **kwargs)
