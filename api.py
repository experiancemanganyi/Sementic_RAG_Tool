# By E.Manganyi
from fastapi import FastAPI
from pydantic import BaseModel
from brain import ask

app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/my_rag")
def ask_question(query: Query):
    answer, sources = ask(query.question)

    return {
        "question": query.question,
        "answer": answer,
        "sources": sources
    }