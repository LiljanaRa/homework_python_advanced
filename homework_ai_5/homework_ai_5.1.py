from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import WebBaseLoader
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=api_key)

loader = WebBaseLoader("https://habr.com/ru/articles/897870/")

docs = loader.load()

prompt = ChatPromptTemplate.from_template("Напиши краткое изложение следующего текста: {context}")

chain = create_stuff_documents_chain(llm, prompt)

result = chain.invoke({"context": docs})

print(result)