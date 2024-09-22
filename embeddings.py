from sentence_transformers import SentenceTransformer
from config import Config

class EmbeddingModel:
    def __init__(self):
        # Load the embedding model
        self.model = SentenceTransformer(Config.EMBEDDING_MODEL)

    def generate_embeddings(self, texts):
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts (list of str): Texts to encode into embeddings.

        Returns:
            list: List of embeddings as tensors.
        """
        return self.model.encode(texts, convert_to_tensor=True)