import httpx


class Automatic1111ImageProvider:

    def __init__(self, base_url: str):

        self.base_url = base_url

    def generate(self, prompt: str) -> str:

        response = httpx.post(
            f"{self.base_url}/sdapi/v1/txt2img",
            json={"prompt": prompt},
            timeout=120,
        )
        response.raise_for_status()

        return response.json()["images"][0]
