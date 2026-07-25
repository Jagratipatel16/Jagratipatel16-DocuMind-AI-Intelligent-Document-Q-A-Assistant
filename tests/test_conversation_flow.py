"""
Tests the full chat-history chain:
create_user -> create_conversation -> save_chat -> get_conversations -> get_user_history

Requires the MySQL database to be reachable and tables created
(`python database/create_tables.py`).
Run with: pytest tests/test_conversation_flow.py
"""

import pytest

from database.database import SessionLocal
from database.crud import create_user, get_user_by_email

from database.conversation_service import create_conversation, get_conversations
from database.chat_service import save_chat, get_messages
from database.history_service import get_user_history


TEST_EMAIL = "test_conversation_flow@example.com"


@pytest.fixture
def test_user():
    db = SessionLocal()

    user = get_user_by_email(db, TEST_EMAIL)

    if user is None:
        user = create_user(
            db,
            name="Test User",
            email=TEST_EMAIL,
            password="test12345"
        )

    db.close()

    return user


def test_create_or_reuse_test_user(test_user):
    assert test_user is not None
    assert test_user.email == TEST_EMAIL


def test_create_conversation(test_user):
    conversation_id = create_conversation(
        test_user.id,
        title="Test Conversation - PDF Q&A"
    )

    assert conversation_id is not None


def test_save_chat_and_fetch_conversations(test_user):
    conversation_id = create_conversation(
        test_user.id,
        title="Test Conversation - Save Chat"
    )

    save_chat(
        conversation_id,
        "What is this document about?",
        "This document is about testing the conversation flow."
    )

    conversations = get_conversations(test_user.id)
    assert len(conversations) > 0
    assert any(c.id == conversation_id for c in conversations)


def test_get_messages_for_conversation(test_user):
    conversation_id = create_conversation(
        test_user.id,
        title="Test Conversation - Messages"
    )

    save_chat(conversation_id, "Question A?", "Answer A.")
    save_chat(conversation_id, "Question B?", "Answer B.")

    messages = get_messages(conversation_id)

    assert len(messages) >= 2
    questions = [m.question for m in messages]
    assert "Question A?" in questions
    assert "Question B?" in questions


def test_get_user_history(test_user):
    conversation_id = create_conversation(
        test_user.id,
        title="Test Conversation - History"
    )

    save_chat(conversation_id, "History question?", "History answer.")

    history = get_user_history(test_user.id)

    assert len(history) > 0
    assert any(h.question == "History question?" for h in history)