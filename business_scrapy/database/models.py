from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()

class SourceData(DeclarativeBase):
    __tablename__ = 'crawler_source'

    id = Column(Integer, primary_key=True)
    name = Column(String(90))
    description = Column(String(65535))
    topics = Column(String(65535))
    source_domain = Column(String(200))
    crawler_url = Column(String(200))
    crawler_schema = Column(String(65535))
    created = Column(Integer(10))
    modified = Column(Integer(10))
    schedule_sync = Column(Integer(10))
    last_sync = Column(Integer(10))
    enabled = Column(Integer(1))

    def __init__(self, id=None, name=None, description=None, topics=None, source_domain=None, crawler_url=None, crawler_schema=None, created=None, modified=None, schedule_sync=None, last_sync=None, enabled=None):
        self.id = id
        self.name = name
        self.description = description
        self.topics = topics
        self.source_domain = source_domain
        self.crawler_url = crawler_url
        self.crawler_schema = crawler_schema
        self.created = created
        self.modified = modified
        self.schedule_sync = schedule_sync
        self.last_sync = last_sync
        self.enabled = enabled

class ListData(DeclarativeBase):
    __tablename__ = 'crawler_list'

class ArticleData(DeclarativeBase):
    __tablename__ = 'crawler_article'