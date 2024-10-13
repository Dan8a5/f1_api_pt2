from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime, timezone

def utc_now():
    return datetime.now(timezone.utc)

class questions(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    question: str
    created_at: datetime = Field(default_factory=utc_now)
    responses: Optional["responses"] = Relationship(back_populates="question")

class responses(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    response_message: str
    created_at: datetime = Field(default_factory=utc_now)
    question_id: Optional[int] = Field(default=None, foreign_key="questions.id")
    question: Optional[questions] = Relationship(back_populates="responses")