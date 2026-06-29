class PromptBuilder:

    def build(
        self,
        conversation,
        message,
        context: list[str] | None = None
    ):

        system_prompt = """
You are an AI assistant.

Be helpful.

Be concise.
"""

        prompt = system_prompt + "\n\n"

        if context:

            prompt += "Relevant context:\n"

            for chunk in context:
                prompt += f"- {chunk}\n"

            prompt += "\n"

        for msg in conversation:

            prompt += f"{msg['role']}: {msg['content']}\n"

        prompt += f"user: {message}"

        return prompt