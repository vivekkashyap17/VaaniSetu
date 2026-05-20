from fastapi import APIRouter

from app.core.vectorstore.embedding_manager import EmbeddingManager

from app.core.vectorstore.faiss_manager import FAISSManager


router = APIRouter()


@router.get("/search")

async def semantic_search(query: str):

    embedding = EmbeddingManager.generate_embedding(
        query
    )

    results = FAISSManager.search_similar(
        embedding
    )

    return {
        "query": query,
        "similar_results": results
    }