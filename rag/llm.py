import os
from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

prompt = ChatPromptTemplate.from_template(
"""
You are an AI assistant.

Answer ONLY using the provided context.

If the answer is not present in the context, reply:

"I could not find the answer in the uploaded document."

Context:
{context}

Question:
{question}
"""
)

chain = prompt | llm

def generate_answer(question, docs):

    context = ""

    for doc in docs:

        context += doc.page_content
        context += "\n\n"

    response = chain.invoke(
        {
            "context": context,
            "question": question
        }
    )

    return response.content