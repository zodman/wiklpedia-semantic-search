import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SCIENTISTS = [
    "Albert Einstein", "Isaac Newton", "Marie Curie", "Charles Darwin"
]
HEADLESS = os.environ.get("HEADLESS")

DATE_FORMAT = "%-d %B %Y"

BASE_DIR = os.path.dirname(__file__)

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV', 'us-central1-gcp')
INDEX_NAME = os.environ.get("PINECONE_DB_NAME", "wikipedia1")
