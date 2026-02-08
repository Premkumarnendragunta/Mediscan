from django.db import models

class Medicine(models.Model):
    name = models.CharField(max_length=120, unique=True)  # Brand name
    generic_name = models.CharField(max_length=120, blank=True)
    uses = models.TextField(blank=True)
    side_effects = models.TextField(blank=True)

    def __str__(self):
        return self.name
