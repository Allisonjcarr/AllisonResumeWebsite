import os
from datetime import datetime
from pytz import timezone
from sqlalchemy import func

from .db import SessionLocal
from .models import WebsiteVisits


# local query uses SQLite
def visits_by_hour_local(db: SessionLocal):
    return (
        db.query(
            func.strftime("%Y-%m-%d %H", WebsiteVisits.visited_at).label("hour"),
            func.count(WebsiteVisits.id).label("visit_count"),
        )
        .group_by(func.strftime("%Y-%m-%d %H", WebsiteVisits.visited_at))
        .order_by(func.strftime("%Y-%m-%d %H", WebsiteVisits.visited_at))
        .all()
    )


# prod query uses Postgres
def visits_by_hour_prod(db: SessionLocal):
    return (
        db.query(
            func.to_char(WebsiteVisits.visited_at, "YYYY-MM-DD HH24").label("hour"),
            func.count(WebsiteVisits.id).label("visit_count"),
        )
        .group_by(func.to_char(WebsiteVisits.visited_at, "YYYY-MM-DD HH24"))
        .order_by(func.to_char(WebsiteVisits.visited_at, "YYYY-MM-DD HH24"))
        .all()
    )


def get_chart_data(db: SessionLocal):
    # visits over time chart
    if os.getenv("ENVIRONMENT") == "prod":
        visits_by_hour = visits_by_hour_prod(db)
    else:
        visits_by_hour = visits_by_hour_local(db)

    est_timezone = timezone("US/Eastern")
    visit_dates = []
    visit_data = []
    for visit in visits_by_hour:
        utc_time = datetime.strptime(visit.hour, "%Y-%m-%d %H")
        est_time = timezone("UTC").localize(utc_time).astimezone(est_timezone)
        formatted_time = est_time.strftime("%m/%d/%Y %I:%M %p")
        visit_dates.append(formatted_time)
        visit_data.append(visit.visit_count)

    # devices chart
    device_counts = (
        db.query(WebsiteVisits.device, func.count(WebsiteVisits.device))
        .group_by(WebsiteVisits.device)
        .all()
    )

    devices = [device for device, _ in device_counts]
    device_counts = [count for _, count in device_counts]

    browser_counts = (
        db.query(WebsiteVisits.browser, func.count(WebsiteVisits.browser))
        .group_by(WebsiteVisits.browser)
        .all()
    )

    browsers = [browser for browser, _ in browser_counts]
    browser_counts = [count for _, count in browser_counts]

    state_counts_query = (
        db.query(WebsiteVisits.state, func.count(WebsiteVisits.state))
        .filter(WebsiteVisits.state.isnot(None))
        .group_by(WebsiteVisits.state)
        .all()
    )

    state_counts = {}
    for state, count in state_counts_query:
        state_counts[state] = count

    country_counts_query = (
        db.query(WebsiteVisits.country, func.count(WebsiteVisits.country))
        .group_by(WebsiteVisits.country)
        .all()
    )

    country_counts = {}
    for country, count in country_counts_query:
        if country in ["US", "United States"]:
            country = "United States of America"
        country_counts[country] = count

    return {
        "visits_table_data": db.query(WebsiteVisits)
        .order_by(WebsiteVisits.id.desc())
        .limit(10)
        .all(),
        "visits_over_time_chart_data": {
            "visit_dates": visit_dates,
            "visit_data": visit_data,
        },
        "devices_chart_data": {
            "devices": devices,
            "counts": device_counts,
        },
        "browsers_chart_data": {"browsers": browsers, "counts": browser_counts},
        "state_chart_data": state_counts,
        "country_chart_data": country_counts,
    }
