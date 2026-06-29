from app.services.image_service import ImageService


class FakeImageProvider:

    def __init__(self):

        self.prompts = []

    def generate(self, prompt: str) -> str:

        self.prompts.append(prompt)

        return "fake-base64-image"


def test_generate_delegates_to_the_image_provider():

    image_provider = FakeImageProvider()
    service = ImageService(image_provider)

    result = service.generate("a cat on a skateboard")

    assert result == "fake-base64-image"
    assert image_provider.prompts == ["a cat on a skateboard"]
