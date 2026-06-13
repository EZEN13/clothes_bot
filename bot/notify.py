from telegram.ext import ContextTypes
from config import MANAGER_CHAT_ID


async def notify_manager(context: ContextTypes.DEFAULT_TYPE, data: dict, kind: str) -> None:
    if not MANAGER_CHAT_ID:
        print(f"[{kind.upper()}] {data}")
        return

    if kind == "order":
        text = (
            "🛍 *Новый заказ с бота*\n\n"
            f"Имя: {data.get('имя', '—')}\n"
            f"Товар: {data.get('товар', '—')}\n"
            f"Размер: {data.get('размер', '—')}\n"
            f"Цвет: {data.get('цвет', '—')}\n"
            f"Доставка: {data.get('доставка', '—')}\n"
            f"Контакт: {data.get('контакт', '—')}"
        )
    else:
        text = (
            "🤝 *Запрос на менеджера*\n\n"
            f"Имя: {data.get('имя', '—')}\n"
            f"Контакт: {data.get('контакт', '—')}\n"
            f"Запрос: {data.get('запрос', '—')}"
        )

    await context.bot.send_message(
        chat_id=MANAGER_CHAT_ID,
        text=text,
        parse_mode="Markdown"
    )
