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


def get_messages(conversation_id):
    """
    Returns all Q&A pairs belonging to one conversation,
    oldest first (for rendering a chat thread top to bottom).
    """

    db = SessionLocal()

    messages = (
        db.query(ChatHistory)
        .filter(ChatHistory.conversation_id == conversation_id)
        .order_by(ChatHistory.created_at.asc())
        .all()
    )

    db.close()

    return messages