from app import db

from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    Text,
    UniqueConstraint,
)

class Student(db.Model):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True, nullable=False)
    token = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    grade = Column(Integer, nullable=False)
    gender = Column(Text, nullable=False)
    school = Column(Text, nullable=False)
    active = Column(Boolean, nullable=False)

    __table_args__ = (UniqueConstraint("email"),)

    def populate(self, token, name, email, password, grade, gender, school, active):
        self.token = token
        self.name = name
        self.email = email
        self.password = password
        self.grade = grade
        self.gender = gender
        self.school = school
        self.active = active
    
    def serialize(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}