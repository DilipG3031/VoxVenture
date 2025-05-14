from django.db import models



class SubjectMaterial(models.Model):
    name = models.CharField(max_length=200)  # Subject name (e.g., 'Theory of Computation')
    pdf = models.FileField(upload_to='pdfs/')  # PDF file
    audio = models.FileField(upload_to='audios/', null=True, blank=True)  # Audio file (e.g., toc.mp3)

    def __str__(self):
        return self.name
