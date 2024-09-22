import re
import logging

logger = logging.getLogger(__name__)

class TextProcessor:
    @staticmethod
    def chunk_into_paragraphs(document_text):
        """
        Split the document text into paragraphs based on double newlines.

        Args:
            document_text (str): The entire document text.

        Returns:
            list of str: A list of paragraphs.
        """
        try:
            paragraphs = re.split(r'\n\s*\n', document_text.strip())
            if not paragraphs:
                logger.warning("No paragraphs found in document.")
            return paragraphs
        except Exception as e:
            logger.error(f"Error while chunking text into paragraphs: {e}")
            raise