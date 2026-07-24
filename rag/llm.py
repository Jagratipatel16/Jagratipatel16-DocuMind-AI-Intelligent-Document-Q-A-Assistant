from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2",
    temperature=0
)

from langchain_core.prompts import ChatPromptTemplate

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