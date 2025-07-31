# shortner/utils.py

import string
import random
from .models import URL  # Import here to avoid circular imports

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits

    while True:
        code = ''.join(random.choice(characters) for _ in range(length))
        if not URL.objects.filter(short_code=code).exists():
            return code
