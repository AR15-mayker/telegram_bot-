async def display_events_page(message, user_id, page):
    from event_manager import EventManager
    events = await EventManager.get_user_events(user_id)
    events_list = list(events.items())
    total_pages = (len(events_list) + 5 - 1) // 5
    page_events = events_list[page*5:(page+1)*5]

    text = "📅 Ваши события:\n\n"
    for i, (event_id, data) in enumerate(page_events, 1):
        reminder = f" (⏰ {data['remind_time'].split()[1]})" if data["remind_time"] else ""
        text += f"{i}. {data['date']} - {data['text']}{reminder}\n"

    kb = get_events_keyboard(events, page)
    await message.answer(f"{text}\nСтраница {page+1}/{total_pages}", reply_markup=kb)