from django.db import models


class TechnicalCompliance (models.Model):
    document_number = models.CharField(max_length=100, unique=True)
    title = models.TextField()
    publication_date = models.DateField()
    html_url = models.URLField(max_length=500)
    abstract = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title