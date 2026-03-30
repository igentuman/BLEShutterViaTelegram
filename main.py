from telegram_listener import start_bot
from ble_keyboard import start_ble

if __name__ == "__main__":
    # Start BLE HID peripheral in background
    start_ble()
    # Start Telegram Bot
    start_bot()
