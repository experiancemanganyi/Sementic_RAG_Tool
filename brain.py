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

def search(query_embedding):
    res = supabase.rpc(
        "match_documents",
        {
            "query_embedding": query_embedding,
            "match_count": 5
        }
    ).execute()
    return res.data

def build_context(docs):
    return "\n\n".join(
        f"[{d['source']} - page {d['page']}]\n{d['content']}"
        for d in docs
    )

def ask(question):
    q_emb = embed(question)
    docs = search(q_emb)

    context = build_context(docs)

    res = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL"),
        messages=[
            {
                "role": "user",
                "content": f"Use ONLY this context:\n{context}\n\nQuestion: {question}"
            }
        ]
    )

    return res.choices[0].message.content, docs