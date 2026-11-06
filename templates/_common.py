"""Shared helpers for templates: date formatting, text defaults, faces."""
import datetime as dt

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def T(ctx, key, default):
    """Text override lookup: ctx['text'][key] or default."""
    return ctx.get("text", {}).get(key, default)


def date_long(d: dt.date):
    return f"{DAYS[d.weekday()]} — {d.day} {MONTHS[d.month - 1][:3]} {d.year}"


def month_name(d: dt.date):
    return MONTHS[d.month - 1]


def week_of(d: dt.date):
    """Monday..Sunday numbers for the week containing d, plus today's index."""
    mon = d - dt.timedelta(days=d.weekday())
    nums = [(mon + dt.timedelta(days=k)).day for k in range(7)]
    return nums, d.weekday()


def face_box(ctx, i=0, default=(0.5, 0.26, 0.26, 0.2)):
    """Normalised face box (cx, cy, w, h) in photo i; from ctx['faces'] if measured, else a default.

    Real-photo work must set ctx['faces'][i] from measurement (page-15 rule 08); defaults are for structure tests.
    """
    faces = ctx.get("faces") or {}
    return faces.get(i, faces.get(str(i), default))


def ordinal(n):
    return f"{n}{'th' if 11 <= n % 100 <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"
