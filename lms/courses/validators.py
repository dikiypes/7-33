from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


class YoutubeLinkValidator:
    def __call__(self, value):
        url_validator = URLValidator()
        try:
            url_validator(value)
        except ValidationError:
            raise ValidationError("Invalid URL")

        if "youtube.com" not in value:
            raise ValidationError("Only YouTube links are allowed")
