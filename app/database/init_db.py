from app.database.base import Base
from app.database.connection import engine

# IMPORTANT
import app.models


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")