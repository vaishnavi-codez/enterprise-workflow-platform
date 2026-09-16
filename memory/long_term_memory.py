from sqlalchemy import select

from config.database import SessionLocal
from memory.database_models import LongTermMemory as MemoryModel


class LongTermMemory:
    """
    Stores important information persistently in PostgreSQL.
    """

    def save_memory(self, session_id: str, content: str):
        db = SessionLocal()

        try:
            memory = MemoryModel(
                session_id=session_id,
                content=content
            )

            db.add(memory)
            db.commit()

        finally:
            db.close()

    def get_memories(self, session_id: str):
        db = SessionLocal()

        try:
            result = db.execute(
                select(MemoryModel)
                .where(MemoryModel.session_id == session_id)
                .order_by(MemoryModel.created_at)
            )

            memories = result.scalars().all()

            return [
                memory.content
                for memory in memories
            ]

        finally:
            db.close()