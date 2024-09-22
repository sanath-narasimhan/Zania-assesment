# Zania Assessment - QA Agent

## Project Description

This project implements a question-answering (QA) agent designed to process PDFs and answer user queries about their content. It leverages various techniques to enhance accuracy and reliability.

## Running Instructions

Clone the Repository:

```bash
git clone https://github.com/sanath-narasimhan/Zania-assesment.git
```

Create a Python Environment and Install Dependencies:

Create a virtual environment using your preferred method (e.g., venv, conda).

Activate the environment.

Install dependencies from the requirements.txt file:

```bash
pip install -r requirements.txt
```

Set Environment Variables:

```bash
Use **set** for Windows and export for macOS/Linux.

Define the following environment variables, replacing placeholders with your actual values:

EMBEDDING_MODEL=all-MiniLM-L6-v2  # Embedding model to use (e.g., for contextualized embeddings)
SIMILARITY_THRESHOLD=0.7        # Minimum similarity score for considering a question match
SLACK_TOKEN=<YOUR SLACK BOT TOKEN>  # Slack bot token for sending notifications
SLACK_CHANNEL=<CHANNEL YOU WANT TO POST TO>  # Slack channel for notifications
LOG_LEVEL=INFO                  # Logging level (e.g., DEBUG, INFO, WARNING, ERROR)
OPENAI_API_KEY=<YOUR OPENAI API KEY>  # OpenAI API key (if using OpenAI models)
OPENAI_MODEL=gpt-4o-mini         # OpenAI model to use (if using OpenAI models)
Navigate to the QA_Agent Directory:

cd QA_Agent
```

## Areas for Improvement

### Word Embeddings:

Employ contextualized embeddings like BERT or GPT-4 for enhanced context understanding.
Fine-tune embeddings on domain-specific datasets (e.g., HR policies, legal documents) for improved term recognition.

### Knowledge Graphs:

Leverage knowledge graphs to represent relationships between entities and answer questions even with slight wording variations.
Enable answer inference based on semantic relations from the knowledge graph.
Support ontologies to address ambiguities and provide structured answers for complex documents.

### Confidence Metric:

Utilize ensemble methods to aggregate results from different models (keyword-based, embedding-based) for more robust confidence scores.
Implement confidence calibration based on document quality and structure (e.g., size, content type, using adaptive thresholds).

### Parsing:

Include an OCR preprocessing step for scanned PDFs to ensure accurate text extraction.
Improve text processing by recognizing document structure (headings, bullet points) for precise paragraph-based chunking and matching.
Modularization and Production-Level Enhancements:

### Scalability:

Implement asynchronous processing for handling large PDFs or multiple requests using asyncio or worker threads.
Enable batch processing for multiple documents and questions using a task queue like Celery to optimize performance.
Utilize cloud storage and caching (e.g., Redis) to store PDFs and parsed text, avoiding redundant parsing.
Consider a microservices architecture, dividing the solution into independent services (PDF extraction, QA, Slack integration) for easier scaling.

## Production-Grade Improvements:

Introduce comprehensive error handling to address network failures, extraction issues, and invalid questions or data.
Implement thorough unit and integration testing:
Unit tests for each module.
Mock the Slack API to test interactions.
Integration tests for the entire flow (PDF parsing to Slack message).
Containerize the solution using Docker for simplified deployment across environments.
Establish automated CI/CD pipelines (e.g., GitHub Actions, CircleCI) for continuous testing and deployment.
Manage and version control fine-tuned models using platforms like Hugging Face Model Hub or MLflow servers (if applicable).
Implement real-time monitoring and alerts for system performance (e.g., with Prometheus and Grafana) to track response times and failures.
