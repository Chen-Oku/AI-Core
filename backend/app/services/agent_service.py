MAX_ITERATIONS = 5


class AgentService:

    def __init__(self, provider, tools, session_manager):

        self.provider = provider
        self.tools = {tool.name: tool for tool in tools}
        self.session_manager = session_manager

    def ask(self, message: str, session_id: str | None) -> tuple[str, str]:

        session_id, memory = self.session_manager.get_or_create(session_id)

        messages = [{"role": m["role"], "content": m["content"]} for m in memory.get_messages()]
        messages.append({"role": "user", "content": message})

        tool_specs = [self._to_spec(tool) for tool in self.tools.values()]

        response = "Could not complete the request within the allowed number of tool calls."

        for _ in range(MAX_ITERATIONS):

            result = self.provider.chat(messages, tools=tool_specs)

            if not result.tool_calls:
                response = result.content
                break

            messages.append({
                "role": "assistant",
                "content": result.content or "",
                "tool_calls": [{"name": c.name, "arguments": c.arguments} for c in result.tool_calls],
            })

            for call in result.tool_calls:
                output = self.tools[call.name].run(**call.arguments)
                messages.append({"role": "tool", "content": output, "tool_name": call.name})

        memory.add_user_message(message)
        memory.add_assistant_message(response)

        return response, session_id

    def _to_spec(self, tool) -> dict:

        return {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters,
            },
        }
