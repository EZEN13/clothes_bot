from telegram import Update
from telegram.ext import ContextTypes
from bot.conversation import get_gemini_response, extract_tag, clean_response
from bot.order import save_order
from bot.notify import notify_manager

user_histories: dict[int, list] = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_histories[user_id] = []
    await update.message.reply_text(
        "Привет! Помогу найти нужную вещь из нашего каталога 👕\n"
        "Что ищете — конкретную модель или просто смотрите что есть?"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_text = update.message.text

    if user_id not in user_histories:
        user_histories[user_id] = []

    user_histories[user_id].append({"role": "user", "content": user_text})
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        response = await get_gemini_response(user_histories[user_id])
    except Exception as e:
        await update.message.reply_text("Что-то пошло не так, попробуйте ещё раз.")
        print(f"Gemini error: {e}")
        return

    order = extract_tag(response, "order_ready")
    lead = extract_tag(response, "lead_ready")

    if order:
        save_order(user_id, order)
        await notify_manager(context, order, kind="order")
    elif lead:
        await notify_manager(context, lead, kind="lead")

    clean = clean_response(response)
    user_histories[user_id].append({"role": "assistant", "content": clean})
    await update.message.reply_text(clean)
