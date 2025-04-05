from langchain_community.document_loaders import PyPDFLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import asyncio
import os
from dotenv import load_dotenv


async def read_pdf():
    loader = PyPDFLoader('romeo-and-juliet.pdf')
    pages = []

    async for page in loader.alazy_load():
        pages.append(page)

    return pages


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = api_key

print('Start reading..')

print('Start embedding..')

result = asyncio.run(read_pdf())
vector_store = InMemoryVectorStore.from_documents(result, GoogleGenerativeAIEmbeddings(model="models/embedding-001"))

query = "Dry sorrow drinks our blood"
docs = vector_store.similarity_search(query, k=2)


for doc in docs:
    print(f'Page {doc.metadata["page"]}: {doc.page_content}\n')