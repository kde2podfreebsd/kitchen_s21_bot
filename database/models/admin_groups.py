from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.orm import relationship

from database.models import Base


class AdminGroups(Base):
    __tablename__ = "admin_groups"

    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger, nullable=False, unique=True)