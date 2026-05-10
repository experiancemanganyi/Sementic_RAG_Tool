# By E.Manganyi
from pypdf import PdfReader
from openai import OpenAI
import os
from dotenv import load_dotenv
from rag import supabase

load_dotenv()
client = OpenAI()

def read_pdfs(folder="data"):
    docs = []

    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            path = os.path.join(folder, file)
            reader = PdfReader(path)

            for i, page in enumerate(reader.pages):
                text = page.extract_text()

                if text:
                    docs.append({
                        "text": text,
                        "source": file,
                        "page": i + 1
                    })

    return docs

def chunk_docs(docs, size=500, overlap=50):
    chunks = []

    for doc in docs:
        text = doc["text"]
        start = 0

        while start < len(text):
            chunks.append({
                "content": text[start:start+size],
                "source": doc["source"],
                "page": doc["page"]
            })
            start += size - overlap

    return chunks

def embed(text):
    res = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return res.data[0].embedding

def store_chunk(chunk, embedding):
    supabase.table("RAG_Table").insert({
        "content": chunk["content"],
        "embedding": embedding,
        "source": chunk["source"],
        "page": chunk["page"]
    }).execute()

if __name__ == "__main__":
    docs = read_pdfs("data")
    chunks = chunk_docs(docs)

    for chunk in chunks:
        emb = embed(chunk["content"])
        store_chunk(chunk, emb)

    print("All PDFs ingested into RAG_Table.")