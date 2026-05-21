from app.core.vectorstore.embedding_manager import EmbeddingManager

from app.core.vectorstore.faiss_manager import FAISSManager


class RetrievalService:


    def retrieve_similar_contexts(
        self,
        text: str,
        top_k: int = 2
    ):

        embedding = EmbeddingManager.generate_embedding(
            text
        )

        similar_results = FAISSManager.search_similar(
            embedding,
            top_k=top_k
        )

        return similar_results