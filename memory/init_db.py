from config.database import engine
from memory.database_models import Base

Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")