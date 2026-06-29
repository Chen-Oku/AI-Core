from fastapi import Depends

from app.core.config import settings
from app.providers.automatic1111_provider import Automatic1111ImageProvider
from app.services.image_service import ImageService


def get_image_provider() -> Automatic1111ImageProvider:

    return Automatic1111ImageProvider(settings.automatic1111_base_url)


def get_image_service(
    image_provider: Automatic1111ImageProvider = Depends(get_image_provider),
) -> ImageService:

    return ImageService(image_provider=image_provider)
