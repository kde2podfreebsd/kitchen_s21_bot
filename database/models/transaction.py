from sqlalchemy import Column, Integer, Float, ForeignKey, BigInteger, DateTime, func
from sqlalchemy.orm import relationship
from database.models import Base


class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    tx_date = Column(DateTime(timezone=True), server_default=func.now())

    client_chat_id = Column(BigInteger, ForeignKey('client.chat_id'), nullable=False)
    client = relationship("Client", back_populates="transactions")