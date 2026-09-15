from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Component(Base):
    """Model pentru cipuri/componente electronice"""
    __tablename__ = "components"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(100), unique=True, index=True)
    name = Column(String(255))
    type = Column(String(50))  # rezistor, tranzistor, capacitor, etc
    specifications = Column(Text, nullable=True)
    datasheet_url = Column(String(500), nullable=True)
    category = Column(String(50), nullable=True)
    manufacturer = Column(String(255), nullable=True)
    price = Column(Float, nullable=True)
    stock = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ScanHistory(Base):
    """Model pentru istoricul scanărilor"""
    __tablename__ = "scan_history"

    id = Column(Integer, primary_key=True, index=True)
    component_id = Column(Integer, index=True, nullable=True)
    scanned_code = Column(String(100), index=True)
    detected_text = Column(Text)
    confidence = Column(Float, default=0.0)
    image_path = Column(String(500), nullable=True)
    found = Column(Boolean, default=False)
    scanned_at = Column(DateTime, default=datetime.utcnow, index=True)


class OCRLog(Base):
    """Model pentru logurile OCR"""
    __tablename__ = "ocr_logs"

    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String(500))
    raw_text = Column(Text)
    processing_time = Column(Float)
    model_used = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
