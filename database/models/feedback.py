from sqlalchemy import Column, Integer,ForeignKey, func, DateTime, Text
from sqlalchemy.orm import relationship

from database.models import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    time = Column(DateTime(timezone=True), server_default=func.now())
    client_id = Column(Integer, ForeignKey('client.chat_id'))

    client = relationship("Client", back_populates="feedbacks")