from sqlalchemy import Column, Integer, String, DateTime
from .db import Base


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
