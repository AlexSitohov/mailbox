import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, TIMESTAMP, text, Integer, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class Mail(Base):
    __tablename__ = "mails"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mail_body = Column(String(500))
    from_email = Column(String, ForeignKey('users.email'))
    to_email = Column(String, ForeignKey('users.email'))
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
