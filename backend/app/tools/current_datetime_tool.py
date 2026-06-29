from datetime import datetime, timezone


class CurrentDateTimeTool:

    name = "current_datetime"
    description = "Get the current date and time (UTC)."
    parameters = {"type": "object", "properties": {}}

    def run(self) -> str:

        return datetime.now(timezone.utc).isoformat()
