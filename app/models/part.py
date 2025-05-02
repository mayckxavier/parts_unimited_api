from sqlalchemy import Column, Integer, String, Boolean

from app.db.base import Base

class Part(Base):
    __tablename__ = "part"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    sku = Column(String(30), unique=True, nullable=False)
    description = Column(String(1024), nullable=True)
    weight_ounces = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)