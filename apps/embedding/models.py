from django.db import models


# Create your models here.类似实体层

class PDFEmbedding(models.Model):
    chunk = models.TextField()
    vector = models.JSONField()

    def __str__(self):
        return self.chunk[:50]
