from .utils import Base62Encoder
from .models import ShortenedURL

class URLShortenerService:
    def __init__(self):
        self.encoder = Base62Encoder()

    def generate_short_url(self, original_url):
        short_url = self.encoder.encode_random()
        while ShortenedURL.objects.filter(short_url=short_url).exists():
            short_url = self.encoder.encode_random()
        return short_url