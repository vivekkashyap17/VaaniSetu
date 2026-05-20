from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float

from app.db.database import Base


class TranslationRecord(Base):


    __tablename__ = "translation_records"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    original_text = Column(String)

    translated_text = Column(String)

    detected_language = Column(String)

    confidence_score = Column(Float)

    processing_time = Column(Float)