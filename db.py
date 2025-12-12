import os
from sqlalchemy import create_engine, Column, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise EnvironmentError("Set DATABASE_URL in environment or .env file")

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

class FormEntry(Base):
    __tablename__ = "form_entries"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    form_type = Column(String, nullable=True)
    image_path = Column(String, nullable=True)
    data = Column(JSONB, nullable=False)

def create_tables():
    # Note: make sure the uuid extension exists in Postgres, see migrations.sql
    Base.metadata.create_all(bind=engine)

class Database:
    def __init__(self):
        create_tables()
        self.session = SessionLocal()

    def save_form(self, form_type, image_path, data):
        entry = FormEntry(form_type=form_type, image_path=image_path, data=data)
        self.session.add(entry)
        self.session.commit()
        self.session.refresh(entry)
        return entry