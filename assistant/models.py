
from django.db import models

class ChatSession(models.Model):
    user_query = models.TextField()
    ai_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_query[:50]
# Create your models here.
