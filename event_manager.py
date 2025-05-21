import uuid
import datetime
from database import Database
from config import ITEMS_PER_PAGE

DELETE_PREFIX = "del_"
REMIND_PREFIX = "rem_"

class EventManager:
    @staticmethod
    async def get_user_events(user_id: int):
        rows = Database.execute_query(
            "SELECT event_id, date, text, remind_time FROM events WHERE user_id = ?",
            (user_id,),
            fetch=True
        )
        return {row[0]: {"date": row[1], "text": row[2], "remind_time": row[3]} for row in rows} if rows else {}

    @staticmethod
    async def add_event(user_id: int, date: str):
        event_id = str(uuid.uuid4())
        Database.execute_query(
            "INSERT INTO events (user_id, event_id, date, text) VALUES (?, ?, ?, ?)",
            (user_id, event_id, date, "Мое событие")
        )
        return event_id

    @staticmethod
    async def update_event_reminder(user_id: int, event_id: str, remind_time: str):
        return Database.execute_query(
            "UPDATE events SET remind_time = ? WHERE user_id = ? AND event_id = ?",
            (remind_time, user_id, event_id)
        ) > 0

    @staticmethod
    async def delete_event(user_id: int, event_id: str):
        return Database.execute_query(
            "DELETE FROM events WHERE user_id = ? AND event_id = ?",
            (user_id, event_id)
        ) > 0

    @staticmethod
    async def clear_user_events(user_id: int):
        count = Database.execute_query(
            "SELECT COUNT(*) FROM events WHERE user_id = ?",
            (user_id,),
            fetch=True
        )[0][0]
        Database.execute_query(
            "DELETE FROM events WHERE user_id = ?",
            (user_id,)
        )
        return count

    @staticmethod
    async def event_exists(user_id: int, date: str) -> bool:
        rows = Database.execute_query(
            "SELECT 1 FROM events WHERE user_id = ? AND date = ? LIMIT 1",
            (user_id, date),
            fetch=True
        )
        return len(rows) > 0

    @staticmethod
    async def get_events_for_reminder():
        now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
        return Database.execute_query(
            "SELECT user_id, text, date FROM events WHERE remind_time = ?",
            (now,),
            fetch=True
        )