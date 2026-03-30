# BLE Shutter Via Telegram

This project allows you to trigger your smartphone's camera shutter remotely using a Telegram bot. It turns your Linux device (with Bluetooth support) into a BLE HID (Human Interface Device) that mimics a volume button press, which most smartphones use as a shutter trigger.

## Features

- **Telegram Interface**: Control your camera shutter from anywhere via Telegram.
- **BLE HID Emulation**: Acts as a standard Bluetooth keyboard/consumer control device.
- **Security**: Optional chat ID filtering to ensure only authorized users can trigger the shutter.

## Prerequisites

- A Linux system with BlueZ (Bluetooth stack) installed.
- Python 3.7+
- A Bluetooth adapter supporting BLE.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/BLEShutterViaTelegram.git
    cd BLEShutterViaTelegram
    ```

2.  **Set up a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure the bot**:
    - Edit `config.py` and add your Telegram Bot Token.
    - Optionally, set `ALLOWED_CHAT_ID` to restrict access.

## Usage

1.  **Start the application**:
    ```bash
    python3 main.py
    ```

2.  **Pair your phone**:
    - On your smartphone, look for a Bluetooth device named **"Lenochka Shutter"**.
    - Pair with it. It should be recognized as a keyboard or input device.

3.  **Trigger the shutter**:
    - Open the Camera app on your phone.
    - Send the message `shut` to your Telegram bot.
    - Your phone will receive a "Volume Up" command and take a photo.

## Configuration

In `config.py`:
- `BOT_TOKEN`: Your Telegram Bot API token from [@BotFather](https://t.me/botfather).
- `ALLOWED_CHAT_ID`: Your Telegram Chat ID. You can find this by sending `/id` to the bot after starting it.

## Troubleshooting

- **Bluetooth permissions**: Ensure the user running the script has permissions to access Bluetooth (often requires being in the `bluetooth` group or running with `sudo` if using certain BlueZ features).
- **Service conflicts**: If the BLE peripheral fails to start, ensure no other HID services are conflicting with BlueZ.
- **Development Note**: In the current version, some BLE calls might be commented out in `main.py` and `telegram_listener.py`. Uncomment them to enable full functionality.

## License

MIT
