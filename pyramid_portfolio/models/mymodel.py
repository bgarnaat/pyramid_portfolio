from sqlalchemy import (
    Column,
    Integer,
    LargeBinary,
    Unicode,
    UnicodeText,
)

from .meta import Base


class Image(Base):
    """docstring for Image"""
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    data = Column(LargeBinary)


class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    description = Column(UnicodeText)
    repository = Column(Unicode)
    website = Column(Unicode)
    image_id = Column(Integer)

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'repository': self.repository,
            'website': self.website,
            'image_id': self.image_id,
        }
