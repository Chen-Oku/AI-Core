class ImageService:

    def __init__(self, image_provider):

        self.image_provider = image_provider

    def generate(self, prompt: str) -> str:

        return self.image_provider.generate(prompt)
