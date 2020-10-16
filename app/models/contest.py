from app import db

from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    Text,
)
from sqlalchemy.dialects.postgresql import ARRAY

class Contest(db.Model):
    __tablename__ = "contest"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(Text, nullable=False)
    body = Column(Text, nullable=False)
    num_questions = Column(Integer, nullable=False)
    answers = Column(ARRAY(Integer), nullable=True)
    active = Column(Boolean, nullable=False)

    def populate(self, name, body, num_questions, answers, active) :
        self.name = name
        self.body = body
        self.num_questions = num_questions
        self.answers = answers
        self.active = active

    def serialize(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}