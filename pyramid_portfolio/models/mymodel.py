from sqlalchemy import (
    Column,
    Integer,
    LargeBinary,
    Unicode,
    UnicodeText,
)

from .meta import Base


class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    description = Column(UnicodeText)
    repository = Column(Unicode)
    website = Column(Unicode)
    image = Column(LargeBinary)

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'repository': self.repository,
            'website': self.website,
        }
