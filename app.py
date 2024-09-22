import logging
import fitz  # PyMuPDF
import openai
from config import Config
from text_processing import TextProcessor
from retrieval import TextRetriever
from slack_interaction import SlackClient


# Set up logging
logging.basicConfig(level=Config.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Temporarly fix warnings of hugginface transformer tockenizer cleanup
import warnings 
warnings.filterwarnings("ignore", category=FutureWarning)

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file using PyMuPDF (fitz).

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF.
    """
    try:
        # Open the PDF file with PyMuPDF
        doc = fitz.open(pdf_path)
        text = ""

        # Iterate through each page and extract text
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text += page.get_text()

        return text
    except Exception as e:
        # Log the error and re-raise the exception
        logger.error(f"Error while extracting text from PDF: {e}")
        raise

def generate_answer_with_openai(question, context):
    """
    Generate an answer to the given question based on the provided context using OpenAI API.

    Args:
        question (str): The question to be answered.
        context (str): The context from which the answer should be derived.

    Returns:
        str: The generated answer or "Data Not Available" if context is not sufficient.
    """
    try:
        # Initialize OpenAI API key. Needs to be turned into a class
        openai.api = Config.OPENAI_API_KEY

        # Send question along with the relevant context from source document to OpenAI model to get the answer
        if context == "Data Not Available":
            return context
        else:
            prompt = f"Answer the following question based on the provided context:\n\nContext: {context}\n\nQuestion: {question}"
            response = openai.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages = [{"role": "user", "content": prompt}]
            )
            print(type(response))
            return response.choices[0].message.content
    except Exception as e:
        # Log the error and re-raise the exception
        logger.error(f"Error while retriving answers from OpenAI call: {e}")
        raise

def process_questions_and_post_to_slack(pdf_path, questions):
    """
    Main function to extract text from a PDF, find relevant answers, and post them to Slack.

    Args:
        pdf_path (str): Path to the PDF document.
        questions (list of str): A list of questions to be answered.

    Returns:
        None
    """
    try:
        # Extract text from the PDF
        document_text = extract_text_from_pdf(pdf_path)

        # Initialize TextProcessor and TextRetriever
        processor = TextProcessor()
        retriever = TextRetriever()
        slack_client = SlackClient()

        #  Process the document text
        paragraphs = processor.chunk_into_paragraphs(document_text)
        if not paragraphs:
            slack_client.post_message("No content found in the document.")
            return

        #  Answer each question and prepare a response message
        response_message = "{"
        for question in questions:
            relevant_paragraph = retriever.find_relevant_paragraphs_w2w(question, paragraphs)
            if relevant_paragraph == "Data Not Available":
                relevant_paragraph = retriever.find_relevant_paragraphs_byEmbedding(question, paragraphs)

            if relevant_paragraph != "Data Not Available":
                answer = generate_answer_with_openai(question,relevant_paragraph)
                response_message += f"\"{question}\" : \"{answer}\",\n"
            else:
                response_message += f"\"{question}\" : \"Data Not Available\",\n"
       

        #  Post the results on Slack
        slack_client.post_message(response_message[:-1] + "}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        slack_client.post_message("An error occurred while processing the document.")

if __name__ == "__main__":
    # Example user input (In production, these inputs would come from a user interface)
    pdf_path = "handbook.pdf"
    questions = [
        "What is the company's vacation policy?",
        "Who is the CEO of the company?",
        "What is the termination policy?"
    ]

    # Call the main function to process the PDF and post the results on Slack
    process_questions_and_post_to_slack(pdf_path, questions)
