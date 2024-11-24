from django.db import models

class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    email = models.EmailField(unique=True)
    website_url = models.URLField()
    established_date = models.DateField(null=True, blank=True)
    sector = models.TextField(blank=True)
    products = models.JSONField(null=True, blank=True)  
    tags = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name
