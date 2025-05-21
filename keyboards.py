from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

DELETE_PREFIX = "del_"
CONFIRM_PREFIX = "cfm_"
CANCEL_PREFIX = "cnl_"
PAGE_PREFIX = "page_"
REMIND_PREFIX = "rem_"

def get_events_keyboard(events, page=0):
    keyboard = []
    total_pages = (len(events) + 5 - 1) // 5
    page_events = list(events.items())[page*5:(page+1)*5]

    for event_id, data in page_events:
        row = [InlineKeyboardButton(text=f"❌ {data['date']}", callback_data=f"{DELETE_PREFIX}{event_id}")]
        if not data['remind_time']:
            row.append(InlineKeyboardButton(text="⏰ Напомнить", callback_data=f"{REMIND_PREFIX}{event_id}"))
        keyboard.append(row)

    pagination = []
    if page > 0:
        pagination.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"{PAGE_PREFIX}{page-1}"))
    if page < total_pages - 1:
        pagination.append(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"{PAGE_PREFIX}{page+1}"))
    if pagination:
        keyboard.append(pagination)

    if events:
        keyboard.append([InlineKeyboardButton(text="🗑️ Очистить всё", callback_data="clear_all")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_confirmation_keyboard(confirm, cancel):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Да", callback_data=confirm),
         InlineKeyboardButton(text="❌ Нет", callback_data=cancel)]
    ])

def get_back_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_events")]
    ])