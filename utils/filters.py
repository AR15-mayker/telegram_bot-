from aiogram.types import Message

async def is_spam(message: Message):
    if any(word in message.text.lower() for word in ["спам", "бесплатно", "член"]):
        return True
    return False