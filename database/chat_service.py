from database.database import SessionLocal
from database.models import ChatHistory


def save_chat(conversation_id, question, answer):

    db = SessionLocal()

    chat = ChatHistory(
        conversation_id=conversation_id,
        question=question,
        answer=answer
    )

    db.add(chat)

    db.commit()

    db.close()