from sqlalchemy import select

from config.database import SessionLocal
from memory.database_models import Conversation


class ShortTermMemory:
    """
    Stores conversation history for the current session
    in PostgreSQL.
    """

    def add_message(self, session_id: str, role: str, content: str):
        db = SessionLocal()

        try:
            message = Conversation(
                session_id=session_id,
                role=role,
                content=content
            )

            db.add(message)
            db.commit()

        finally:
            db.close()

    def get_history(self, session_id: str):
        db = SessionLocal()

        try:
            result = db.execute(
                select(Conversation)
                .where(Conversation.session_id == session_id)
                .order_by(Conversation.created_at)
            )

            messages = result.scalars().all()

            return [
                {
                    "role": message.role,
                    "content": message.content
                }
                for message in messages
            ]

        finally:
            db.close()

    def clear_session(self, session_id: str):
        db = SessionLocal()

        try:
            db.query(Conversation).filter(
                Conversation.session_id == session_id
            ).delete()

            db.commit()

        finally:
            db.close()