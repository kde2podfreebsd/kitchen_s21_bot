from sqlalchemy import Column, Integer, String, BigInteger, Boolean, Date
from sqlalchemy.orm import relationship

from database.models import Base


class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger, nullable=False, unique=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    donation_status = Column(Boolean, default=False, nullable=False)
    next_donation_time = Column(Date)

    transactions = relationship("Transaction", back_populates="client")
    feedbacks = relationship("Feedback", back_populates="client")
