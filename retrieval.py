import re
import logging
from sentence_transformers import util
from config import Config
from embeddings import EmbeddingModel

logger = logging.getLogger(__name__)

class TextRetriever:
    def __init__(self):
        # Initialize the embedding model
        self.embedding_model = EmbeddingModel()

    def find_relevant_paragraphs_w2w(self, question, paragraphs):
        """
        Find the most relevant paragraphs from the document based on word-to-word matching.

        Args:
            question (str): The user's question.
            paragraphs (list of str): List of document paragraphs.

        Returns:
            str: The most relevant paragraph or "Data Not Available" if none are relevant.
        """
        try:
            # Extract keywords from the question (words longer than 3 characters)
            question_keywords = [word for word in re.findall(r'\b\w{4,}\b', question.lower())]

            # Search for relevant paragraphs containing any of the question keywords
            relevant_paragraphs = []
            for paragraph in paragraphs:
                paragraph_lower = paragraph.lower()
                if any(keyword in paragraph_lower for keyword in question_keywords):
                    relevant_paragraphs.append(paragraph)

            # Return the paragraph with the highest number of keyword matches
            if relevant_paragraphs:
                # Optionally, you could rank by number of matches
                sorted_paragraphs = sorted(relevant_paragraphs, key=lambda p: sum(k in p.lower() for k in question_keywords), reverse=True)
                return sorted_paragraphs[0]  # Return the top-ranking paragraph
            else:
                return "Data Not Available"

        except Exception as e:
            logger.error(f"Error while retrieving relevant paragraphs: {e}")
            raise

    def find_relevant_paragraphs_byEmbedding(self, question, paragraphs):
        """
        Find the most relevant paragraphs from the document based on semantic similarity.

        Args:
            question (str): The user's question.
            paragraphs (list of str): List of document paragraphs.

        Returns:
            str: The most relevant paragraph or "Data Not Available" if none are relevant.
        """
        try:
            # Generate embeddings for the question and the paragraphs
            question_embedding = self.embedding_model.generate_embeddings([question])
            paragraph_embeddings = self.embedding_model.generate_embeddings(paragraphs)

            # Compute cosine similarity between question and each paragraph
            cosine_scores = util.pytorch_cos_sim(question_embedding, paragraph_embeddings)[0]

            # Retrieve paragraphs with similarity above the threshold
            relevant_paragraphs = []
            for i, score in enumerate(cosine_scores):
                if score > Config.SIMILARITY_THRESHOLD:
                    relevant_paragraphs.append((paragraphs[i], score.item()))

            # Return the highest scoring relevant paragraph or "Data Not Available"
            if relevant_paragraphs:
                relevant_paragraphs = sorted(relevant_paragraphs, key=lambda x: x[1], reverse=True)
                return relevant_paragraphs[0][0]  # Return the top-scoring paragraph
            else:
                return "Data Not Available"

        except Exception as e:
            logger.error(f"Error while retrieving relevant paragraphs: {e}")
            raise