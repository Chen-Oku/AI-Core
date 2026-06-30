from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_tenant
from app.dependencies.image import get_image_service
from app.schemas.image_schema import ImageGenerateRequest, ImageGenerateResponse
from app.services.image_service import ImageService

router = APIRouter()


@router.post("/images/generate", response_model=ImageGenerateResponse)
def generate(
    request: ImageGenerateRequest,
    _tenant: str = Depends(get_current_tenant),
    image_service: ImageService = Depends(get_image_service)
):

    image_base64 = image_service.generate(request.prompt)

    return ImageGenerateResponse(image_base64=image_base64)
