import chromadb
import os

class LongTermMemory:
    """
    Manages persistent vector storage for The Sovereign Conglomerate.
    Allows agents to recall past projects, templates, and successful architectures.
    """
    def __init__(self, persist_directory="./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name="successful_operations")

    def store_project(self, project_id: str, scope: str, deliverable: str):
        """Stores a completed project in long-term memory."""
        document = f"SCOPE:\n{scope}\n\nDELIVERABLE:\n{deliverable}"
        self.collection.upsert(
            documents=[document],
            metadatas=[{"type": "project_history", "status": "APPROVED"}],
            ids=[project_id]
        )

    def recall(self, query: str, n_results: int = 3):
        """Recalls relevant past project contexts based on a semantic query."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        if results['documents']:
            return results['documents'][0]
        return []

# Singleton instance for the framework
memory_bank = LongTermMemory()
