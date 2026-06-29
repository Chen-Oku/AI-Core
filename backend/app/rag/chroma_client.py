import chromadb
from chromadb.api import ClientAPI
from chromadb.api.models.Collection import Collection


def create_chroma_client(host: str, port: int) -> ClientAPI:

    return chromadb.HttpClient(host=host, port=port)


def get_or_create_collection(client: ClientAPI, name: str) -> Collection:

    return client.get_or_create_collection(name)
