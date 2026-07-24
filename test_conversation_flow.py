"""
Tests the full chat-history chain:
create_user -> create_conversation -> save_chat -> get_conversations -> get_user_history

Run this AFTER applying the app.py / crud.py fixes, and after
`python database/create_tables.py` has been run at least once.
"""

from database.database import SessionLocal
from database.crud import create_user, get_user_by_email

from database.conversation_service import create_conversation, get_conversations
from database.chat_service import save_chat
from database.history_service import get_user_history


TEST_EMAIL = "test_conversation_flow@example.com"


def get_or_create_test_user():

    db = SessionLocal()

    user = get_user_by_email(db, TEST_EMAIL)

    if user is None:
        user = create_user(
            db,
            name="Test User",
            email=TEST_EMAIL,
            password="test12345"
        )
        print("✅ Created new test user")
    else:
        print("ℹ️  Reusing existing test user")

    db.close()

    return user


def main():

    # 1. User
    user = get_or_create_test_user()
    assert user is not None, "❌ Failed to get/create test user"
    print(f"User ID: {user.id}, Email: {user.email}")
    print()

    # 2. Conversation
    conversation_id = create_conversation(
        user.id,
        title="Test Conversation - PDF Q&A"
    )
    assert conversation_id is not None, "❌ create_conversation returned None"
    print(f"✅ Conversation created, ID: {conversation_id}")
    print()

    # 3. Save a chat message under that conversation
    save_chat(
        conversation_id,
        "What is this document about?",
        "This document is about testing the conversation flow."
    )
    print("✅ Chat saved under conversation")
    print()

    # 4. Fetch conversations for the user
    conversations = get_conversations(user.id)
    assert len(conversations) > 0, "❌ No conversations found for user"
    print(f"✅ get_conversations() returned {len(conversations)} conversation(s)")
    for c in conversations:
        print(f"   - [{c.id}] {c.title}")
    print()

    # 5. Fetch chat history (joins ChatHistory -> Conversation -> User)
    history = get_user_history(user.id)
    assert len(history) > 0, "❌ No chat history found for user"
    print(f"✅ get_user_history() returned {len(history)} message(s)")
    for h in history:
        print(f"   Q: {h.question}")
        print(f"   A: {h.answer}")

    print()
    print("🎉 All checks passed — chat history chain is working correctly!")


if __name__ == "__main__":
    main()