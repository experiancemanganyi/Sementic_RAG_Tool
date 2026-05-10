# By E.Manganyi
from openai import OpenAI
from rag import supabase
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def embed(text):
    res = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return res.data[0].embedding

def search(query_embedding, source_filter=None):
    return supabase.rpc(
        "match_documents",
        {
            "query_embedding": query_embedding,
            "match_count": 5,
            "filter_source": source_filter
        }
    ).execute()

def build_context(docs):
    return "\n\n".join([
        f"[{doc['source']} - page {doc['page']}]\n{doc['content']}"
        for doc in docs
    ])

def ask(query):
    query_emb = embed(query)

    results = search(query_emb)
    docs = results.data

    context = build_context(docs)

    prompt = f"""
Use ONLY the context below to answer.

Context:
{context}

Question:
{query}
"""

    res = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL"),
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content

if __name__ == "__main__":
    q = input("Ask: ")
    print(ask(q))