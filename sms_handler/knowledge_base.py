import chromadb
from chromadb.utils import embedding_functions
import google.generativeai as genai
from django.conf import settings


genai.configure(api_key=settings.GOOGLE_API_KEY)

def embed_text(texts):
    model = genai.GenerativeModel('embedding-001')
    embeddings = []
    for text in texts:
        response = model.embed_content(
            content=text,
            task_type="retrieval_document",
            title="Knowledge Base Entry"
        )
        embeddings.append(response['embedding'])
    return embeddings


# Initialize ChromaDB client
client = chromadb.Client()

# Create collection (or get existing one)
collection = client.get_or_create_collection(name="knowledge_base")

# Your small knowledge base (for now, static; later from DB)
documents = [
    "To register a business in Uganda, visit the Uganda Registration Services Bureau (URSB) website.",
    "The school term dates for 2025 start in February and end in November.",
    "The official emergency number for Uganda is 999 or 112.",
    "To renew a driving permit in Uganda, visit Face Technologies offices with your National ID.",
    "Agricultural loans are available from Centenary Bank and PostBank Uganda."
]