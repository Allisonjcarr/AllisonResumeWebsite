from sqlalchemy import Column, Integer, String, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class WebsiteVisits(Base):
    __tablename__ = "website_visits"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String)
    user_agent_string = Column(String)
    device = Column(String)
    browser = Column(String)
    city = Column(String)
    state = Column(String)
    visited_at = Column(DateTime)
    endpoint = Column(String)


DATABASE_URL = "sqlite:///./website.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session_local():
    yield SessionLocal()
