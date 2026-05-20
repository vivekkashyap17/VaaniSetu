from sentence_transformers import SentenceTransformer


class EmbeddingManager:


    embedding_model = None


    @classmethod
    def load_embedding_model(cls):

        if cls.embedding_model is None:

            print("Loading embedding model...")

            cls.embedding_model = SentenceTransformer(
                "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
            )

            print("Embedding model loaded.")


    @classmethod
    def generate_embedding(
        cls,
        text: str
    ):

        embedding = cls.embedding_model.encode(text)

        return embedding