import os
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.runnable import Runnable
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
assert GROQ_API_KEY is not None, "Missing GROQ_API_KEY in .env"

# Initialize HuggingFace embedding model (Free)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Load and split schema file
def load_schema_chunks():
    loader = TextLoader("data/schema.txt")
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    return splitter.split_documents(docs)

# Build or load Chroma vectorstore
def get_vectorstore():
    persist_path = "vectorstore/chroma"
    if not os.path.exists(persist_path):
        os.makedirs(persist_path)

    if len(os.listdir(persist_path)) == 0:
        # First time: create and persist
        print("Creating new Chroma vectorstore...")
        documents = load_schema_chunks()
        vectorstore = Chroma.from_documents(documents, embeddings, persist_directory=persist_path)
        vectorstore.persist()
    else:
        # Load from disk
        vectorstore = Chroma(persist_directory=persist_path, embedding_function=embeddings)
    
    return vectorstore

# Prompt template
TEMPLATE = """
You are a SQL expert. Based on the database schema context below, convert the natural language question into an accurate SQL query.

IMPORTANT:
- Only return the raw SQL query.
- Do NOT include explanations, markdown, or anything else.
- Do NOT use triple backticks or comments.
- Just return the SQL.

Schema:
{context}

Question: {question}

SQL:
"""


prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=TEMPLATE
)

def generate_sql_query(user_question: str) -> str:
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_type="similarity", k=4)
    results = retriever.get_relevant_documents(user_question)
    schema_context = "\n".join([doc.page_content for doc in results])

    full_prompt = prompt.format(context=schema_context, question=user_question)

    llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0)
    messages = [
        SystemMessage(content="You are an expert SQL data analyst."),
        HumanMessage(content=full_prompt),
    ]
    sql = llm(messages).content.strip()
    return sql
