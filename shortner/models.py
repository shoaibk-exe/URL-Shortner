from django.db import models
from django.contrib.auth.models import User
import random
import string

def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

class URL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True, default=generate_short_code)
    created_at = models.DateTimeField(auto_now_add=True)
    click_count = models.IntegerField(default=0)

    def get_short_url(self):
        return f"http://127.0.0.1:8000/u/{self.short_code}"
