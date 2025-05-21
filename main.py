import asyncio
import logging
import uuid
import random
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback
from aiogram.types import ReplyKeyboardRemove
from loguru import logger
from config import BOT_TOKEN, REMINDER_CHECK_INTERVAL
from event_manager import EventManager
from keyboards import get_events_keyboard, get_confirmation_keyboard, get_back_keyboard
from message_manager import display_events_page
import database

# Настройка логгера
logger.add("bot.log", format="{time} | {level} | {message}", level="DEBUG")

# Инициализация
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
remind_data = {}

# Команды
@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    logger.info(f"User {message.from_user.id} started the bot")
    await message.answer(
        "📅 Бот-календарь с напоминаниями\n"
        "Доступные команды:\n"
        "/calendar - добавить дату\n"
        "/myevents - мои события\n"
        "/today - сегодняшняя дата\n"
        "/clearevents - очистить все события",
        reply_markup=ReplyKeyboardRemove()
    )

@dp.message(Command("today"))
async def today_cmd(message: types.Message):
    await message.answer(f"📆 Сегодня: {datetime.now().strftime('%d.%m.%Y')}")

@dp.message(Command("calendar"))
async def calendar_cmd(message: types.Message):
    logger.info(f"User {message.from_user.id} opened calendar")
    await message.answer("Выберите дату:", reply_markup=await SimpleCalendar().start_calendar())

@dp.message(Command("myevents"))
async def show_events(message: types.Message):
    user_id = message.from_user.id
    if not await EventManager.get_user_events(user_id):
        await message.answer("📭 Нет событий.")
        return
    await display_events_page(message, user_id, 0)

# Callbacks
@dp.callback_query(SimpleCalendarCallback.filter())
async def process_calendar(callback_query: types.CallbackQuery, callback_data: SimpleCalendarCallback):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        user_id = callback_query.from_user.id
        date_str = date.strftime('%d.%m.%Y')
        if await EventManager.event_exists(user_id, date_str):
            await callback_query.message.answer("⚠️ Такая дата уже есть!")
        else:
            event_id = await EventManager.add_event(user_id, date_str)
            await callback_query.message.answer(f"✅ Дата {date_str} добавлена!")

# Напоминания
async def remind_checker():
    while True:
        try:
            events = await EventManager.get_events_for_reminder()
            for user_id, text, date in events:
                try:
                    await bot.send_message(user_id, f"⏰ Напоминание!\n{date} - {text}")
                except Exception as e:
                    logger.error(f"Ошибка при отправке напоминания пользователю {user_id}: {e}")
        except Exception as e:
            logger.error(f"Ошибка в remind_checker: {e}")
        await asyncio.sleep(REMINDER_CHECK_INTERVAL)

async def main():
    database.Database.init_db()
    dp.startup.register(lambda: logger.info("Bot started"))
    dp.shutdown.register(lambda: logger.warning("Bot stopped"))
    asyncio.create_task(remind_checker())
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")