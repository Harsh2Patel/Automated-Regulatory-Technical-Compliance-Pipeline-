from django.db import models

class TechnicalCompliance(models.Model):
    title = models.TextField()
    publication_date = models.DateField()
    html_url = models.URLField(max_length=500)
    abstract = models.TextField(blank=True, null=True)
    # This line tells the database to automatically stamp the exact time a record is fetched
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title