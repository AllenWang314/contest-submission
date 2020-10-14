from app import db

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    Numeric,
    Text,
    UniqueConstraint,
)

from sqlalchemy.dialects.postgresql import ARRAY

class Submission(db.Model):

    id = Column(Integer, primary_key=True, nullable=False)
    student_id = Column(Integer, ForeignKey("student.id"), nullable=False)
    contest_id = Column(Integer, ForeignKey("contest.id"), nullable=False)
    answers = Column(ARRAY(Integer), nullable=True)
    raw_score = Column(Numeric, nullable=True)
    adj_score = Column(Numeric, nullable=True)

    __table_args__ = (UniqueConstraint("student_id", "contest_id"),)

    def populate(self, student_id, contest_id, answers, raw_score, adj_score):
        self.student_id = student_id
        self.contest_id = contest_id
        self.answers = answers,
        self.raw_score = raw_score
        self.adj_score = adj_score

    def serialized(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


