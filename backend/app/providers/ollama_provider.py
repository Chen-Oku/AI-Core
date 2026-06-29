from ollama import chat

class OllamaProvider:
    def generate(self, prompt: str) -> str:

        responses = chat(
            model="qwen3:latest",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return responses.message.content