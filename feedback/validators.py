from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


MAX_IMAGE_UPLOAD_SIZE = 5 * 1024 * 1024


def validate_image_size(image):
    if image.size > MAX_IMAGE_UPLOAD_SIZE:
        raise ValidationError(
            _("A imagem deve ter no máximo 5 MB."),
            code="image_too_large",
        )
