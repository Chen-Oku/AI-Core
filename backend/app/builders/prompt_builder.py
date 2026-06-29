class PromptBuilder:

    def build(
        self,
        conversation,
        message
    ):

        system_prompt = """
You are an AI assistant.

Be helpful.

Be concise.
"""

        prompt = system_prompt + "\n\n"

        for msg in conversation:

            prompt += f"{msg['role']}: {msg['content']}\n"

        prompt += f"user: {message}"

        return prompt