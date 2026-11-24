"""Turn raw USAJOBS Search API results into clean posting records.

A record keeps the fields the dashboard needs (title, agency, job series, grade,
location, dates) and one cleaned text made of the summary, duties and qualifications.
Contact details are removed before anything is stored.
"""
from __future__ import annotations

import html
import re

_TAG = re.compile(r"<[^>]+>")
_EMAIL = re.compile(r"[\w.+-]+@[\w-]+(\.[\w-]+)+")
_PHONE = re.compile(r"(\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}")
_URL = re.compile(r"https?://\S+|www\.\S+")
_SPACE = re.compile(r"\s+")
_SENT_END = re.compile(r"(?<=[.!?;])\s+(?=[A-Z0-9(\"'])")


def clean_text(text: str) -> str:
    """Strip HTML, contact details and links; collapse whitespace."""
    text = html.unescape(text or "")
    text = _TAG.sub(" ", text)
    text = _EMAIL.sub(" ", text)
    text = _URL.sub(" ", text)
    text = _PHONE.sub(" ", text)
    return _SPACE.sub(" ", text).strip()


def split_sentences(text: str) -> list[str]:
    """Simple sentence split; also splits bullet-style lists written with ' - ' or '•'."""
    parts: list[str] = []
    for chunk in re.split(r"\s[•·▪]\s|\s-\s(?=[A-Z])", text):
        parts.extend(p.strip() for p in _SENT_END.split(chunk))
    return [p for p in parts if len(p.split()) >= 3]


def _first(items, key: str = "Code") -> str:
    if isinstance(items, list) and items:
        first = items[0]
        return str(first.get(key, "")) if isinstance(first, dict) else str(first)
    return ""


def parse_item(item: dict) -> dict:
    """One SearchResultItems entry -> one flat record with cleaned text."""
    d = item.get("MatchedObjectDescriptor", {})
    details = (d.get("UserArea") or {}).get("Details") or {}
    duties = details.get("MajorDuties") or []
    if isinstance(duties, str):
        duties = [duties]
    pieces = [details.get("JobSummary", ""), *duties, d.get("QualificationSummary", "")]
    text = clean_text(" ".join(p for p in pieces if p))
    return {
        "usajobs_id": str(item.get("MatchedObjectId") or d.get("PositionID", "")),
        "title": d.get("PositionTitle", ""),
        "organization": d.get("OrganizationName", ""),
        "department": d.get("DepartmentName", ""),
        "job_series": _first(d.get("JobCategory")),
        "job_series_name": _first(d.get("JobCategory"), "Name"),
        "grade": _first(d.get("JobGrade")) + (f"-{details.get('LowGrade')}" if details.get("LowGrade") else ""),
        "location": d.get("PositionLocationDisplay", ""),
        "posted": (d.get("PublicationStartDate") or "")[:10],
        "closes": (d.get("ApplicationCloseDate") or "")[:10],
        "url": d.get("PositionURI", ""),
        "text": text,
        "sentences": split_sentences(text),
    }
