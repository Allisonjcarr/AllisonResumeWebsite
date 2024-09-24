from datetime import datetime
from pytz import timezone
from sqlalchemy import func

from .db import SessionLocal
from .models import WebsiteVisits


def get_chart_data(db: SessionLocal):
    # visits over time chart
    visits_by_hour = (
        db.query(
            func.strftime("%Y-%m-%d %H", WebsiteVisits.visited_at).label("hour"),
            func.count(WebsiteVisits.id).label("visit_count"),
        )
        .group_by(func.strftime("%Y-%m-%d %H", WebsiteVisits.visited_at))
        .order_by(func.strftime("%Y-%m-%d %H", WebsiteVisits.visited_at))
        .all()
    )

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
    counts = [count for _, count in device_counts]

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
            "counts": counts,
        },
    }
