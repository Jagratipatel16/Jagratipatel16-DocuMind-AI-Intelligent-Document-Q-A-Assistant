from database.database import SessionLocal
from database.models import Conversation
from database.models import ChatHistory


def get_user_history(user_id):

    db = SessionLocal()

    history = (
        db.query(ChatHistory)
        .join(Conversation)
        .filter(Conversation.user_id == user_id)
        .order_by(ChatHistory.created_at.desc())
        .all()
    )

    db.close()

    return history