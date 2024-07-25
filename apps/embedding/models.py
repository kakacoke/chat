from django import forms
from django.db import models


# Create your models here.类似实体层

class PDFDocument(models.Model):
    title = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='pdfs/')

    def __str__(self):
        return self.title


class PDFUploadForm(forms.ModelForm):
    class Meta:
        model = PDFDocument
        fields = ['title', 'pdf']
