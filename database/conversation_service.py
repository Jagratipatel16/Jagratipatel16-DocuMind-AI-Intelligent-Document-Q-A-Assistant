from database.database import SessionLocal
from database.models import Conversation


def create_conversation(user_id, title):

    db = SessionLocal()

    conversation = Conversation(
        user_id=user_id,
        title=title
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    db.close()

    return conversation.id

def get_conversations(user_id):

    db = SessionLocal()

    conversations = (
        db.query(Conversation)
        .filter(Conversation.user_id == user_id)
        .order_by(Conversation.created_at.desc())
        .all()
    )

    db.close()

    return conversations


def delete_conversation(conversation_id):
    """
    Deletes a conversation and (via cascade in models.py)
    all of its chat messages too.
    """

    db = SessionLocal()

    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).first()

    if conversation:
        db.delete(conversation)
        db.commit()

    db.close()