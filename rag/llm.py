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


# -----------------------------------
# Document Summarizer
# -----------------------------------

summary_prompt = ChatPromptTemplate.from_template(
"""
You are an AI assistant that writes clear, well-structured summaries.

Summarize the following document in 150-250 words.

Structure your summary as:
1. A short overview (2-3 sentences)
2. Key points as bullet points (4-6 bullets)

Document:
{document_text}
"""
)

summary_chain = summary_prompt | llm

def generate_summary(document_text):

    # Guard against extremely long documents overflowing the
    # model's context window — trim to a safe character budget.
    max_chars = 15000

    if len(document_text) > max_chars:
        document_text = document_text[:max_chars] + "\n\n[...document truncated for summarization...]"

    response = summary_chain.invoke(
        {
            "document_text": document_text
        }
    )

    return response.content