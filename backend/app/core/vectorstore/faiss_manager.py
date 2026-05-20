import faiss
import numpy as np


class FAISSManager:


    index = None

    stored_texts = []


    @classmethod
    def initialize_index(cls):

        if cls.index is None:

            dimension = 384

            cls.index = faiss.IndexFlatL2(dimension)

            print("FAISS index initialized.")


    @classmethod
    def add_embedding(
        cls,
        embedding,
        text: str
    ):

        vector = np.array(
            [embedding],
            dtype="float32"
        )

        cls.index.add(vector)

        cls.stored_texts.append(text)


    @classmethod
    def search_similar(
        cls,
        embedding,
        top_k: int = 3
    ):

        vector = np.array(
            [embedding],
            dtype="float32"
        )

        distances, indices = cls.index.search(
            vector,
            top_k
        )

        results = []


        for idx in indices[0]:

            if idx < len(cls.stored_texts):

                results.append(
                    cls.stored_texts[idx]
                )


        return results