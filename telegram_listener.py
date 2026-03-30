from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters
from ble_keyboard import send_shutter
from config import BOT_TOKEN, ALLOWED_CHAT_ID

async def start(update: Update, context):
    await update.message.reply_text(
        "Welcome to Lenochka Photo Bot!\n\n"
        "1. Pair your phone with this laptop via Bluetooth.\n"
        "2. Open the Camera app on your phone.\n"
        "3. Send 'shut' to take a photo!\n\n"
        "Use /id to get your Chat ID for security configuration."
    )

async def get_id(update: Update, context):
    await update.message.reply_text(f"Your Chat ID is: {update.effective_chat.id}")

async def handle(update: Update, context):
    # Security filter
    if ALLOWED_CHAT_ID is not None and update.effective_chat.id != ALLOWED_CHAT_ID:
        print(f"Unauthorized access from chat id: {update.effective_chat.id}")
        return

    if not update.message or not update.message.text:
        return

    text = update.message.text.lower().strip()

    if text == "shut":
        print("Shutter command received")
        send_shutter()
        await update.message.reply_text("Click!")

def start_bot():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("id", get_id))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    
    print("Bot started. Listening for commands...")
    app.run_polling()
