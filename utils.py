from datetime import datetime, time
from zoneinfo import ZoneInfo


TIMEZONE = ZoneInfo("Europe/Kiev")
WORK_START = time(9, 0)
WORK_END = time(19, 0)

def is_working_hours() -> bool:
    now = datetime.now(TIMEZONE).time()
    return WORK_START <= now < WORK_END
