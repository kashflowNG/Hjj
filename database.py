
import os
from datetime import datetime
from sqlalchemy import create_engine, Column, String, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    pin_hash = Column(String, nullable=False)
    password_hash = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    wallets = relationship("Wallet", back_populates="user", cascade="all, delete-orphan")

class Wallet(Base):
    __tablename__ = "wallets"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False, index=True)
    private_key = Column(String, nullable=False)
    hex_address = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="wallets")

class DemoProfile(Base):
    __tablename__ = "demo_profiles"
    
    id = Column(String, primary_key=True, index=True)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    wallet_address = Column(String, nullable=False)
    balance_trx = Column(Float, nullable=False)
    balance_usdt = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)
