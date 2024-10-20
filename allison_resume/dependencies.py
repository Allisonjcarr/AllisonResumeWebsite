import requests
from fastapi import Request, Depends
from datetime import datetime
from .models import WebsiteVisits
from .db import SessionLocal, get_session_local
from user_agents import parse


def get_location_from_ip(ip: str):
    try:
        ip = "173.246.203.9"
        # You can sign up for a free API key from ipapi or any other IP location service
        response = requests.get(f"http://ipapi.co/{ip}/json/")
        data = response.json()

        city = data.get("city", "Unknown")
        state = data.get("region", "Unknown")
        country = data.get("country", "Unknown")
        return city, state, country
    except:
        return "Unknown", "Unknown", "Unknown"


# Dependency to log each visit
def log_visit(request: Request, db: SessionLocal = Depends(get_session_local)):
    ip = request.client.host
    city, state, country = get_location_from_ip(ip)

    user_agent_string = request.headers.get("User-Agent", "Unknown")
    user_agent = parse(user_agent_string)
    browser = user_agent.browser.family  # Browser name (e.g., "Chrome")
    device = (
        "Mobile"
        if user_agent.is_mobile
        else "Tablet" if user_agent.is_tablet else "Desktop"
    )

    endpoint = request.url.path
    visited_at = datetime.utcnow()

    visit = WebsiteVisits(
        ip=ip,
        user_agent_string=user_agent_string,
        city=city,
        state=state,
        country=country,
        device=device,
        browser=browser,
        visited_at=visited_at,
        endpoint=endpoint,
    )

    db.add(visit)
    db.commit()
    db.close()
