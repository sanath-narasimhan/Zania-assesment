import os

class Config:
    # Model settings
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')

    # Similarity threshold for finding relevant paragraphs
    SIMILARITY_THRESHOLD = float(os.getenv('SIMILARITY_THRESHOLD', 0.7))

    # Slack API settings
    SLACK_TOKEN = os.getenv('SLACK_TOKEN')
    SLACK_CHANNEL = os.getenv('SLACK_CHANNEL', '#general')

    # Logging settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    # OpenAI API Key
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL','gpt-4o-mini')