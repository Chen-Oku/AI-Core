class RagSearchTool:

    name = "rag_search"
    description = "Search the knowledge base for relevant information from previously ingested documents."
    parameters = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "What to search for"}
        },
        "required": ["query"],
    }

    def __init__(self, rag_service, tenant: str):

        self.rag_service = rag_service
        self.tenant = tenant

    def run(self, query: str) -> str:

        chunks = self.rag_service.retrieve(query, self.tenant)

        return "\n".join(chunks) if chunks else "No relevant information found."
