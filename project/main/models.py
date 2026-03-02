from django.db import models


class ContactMessage(models.Model):
    first_name = models.CharField(max_length=80,  verbose_name="Prénom")
    last_name  = models.CharField(max_length=80,  verbose_name="Nom")
    email      = models.EmailField(               verbose_name="Email")
    phone      = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    message    = models.TextField(               verbose_name="Message")
    is_read    = models.BooleanField(default=False, verbose_name="Lu")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Reçu le")

    class Meta:
        verbose_name        = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering            = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} — {self.email}"
