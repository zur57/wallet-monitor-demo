import os
import subprocess
import sys

# --- Auto-install required packages ---
try:
    from dotenv import load_dotenv
except ImportError:
    print("Installing required package: python-dotenv...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])
    from dotenv import load_dotenv

try:
    import requests
except ImportError:
    print("Installing required package: requests...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

# --- Load environment variables ---
load_dotenv("config.env")

WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
PRICE_API_KEY = os.getenv("PRICE_API_KEY")

# --- Load optional thresholds ---
def get_threshold(token):
    key = f"{token.upper()}_ALERT_THRESHOLD"
    value = os.getenv(key)
    return float(value) if value else None

# --- Simulated Wallet Parser ---
def get_wallet_data(wallet_address):
    return {
        "SOL": 2.5,
        "USDC": 100,
        "BONK": 500000
    }

# --- Simulated Price Fetcher ---
def get_token_prices():
    return {
        "SOL": 24.3,
        "USDC": 1.0,
        "BONK": 0.0000012
    }

# --- Smart Telegram Alert ---
def send_alert(message):
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }
        try:
            response = requests.post(url, data=payload)
            if response.status_code != 200:
                print(f"[Telegram Error] {response.text}")
        except Exception as e:
            print(f"[Telegram Exception] {e}")
    else:
        print(f"[Simulated Telegram] {message}")

# --- Main Logic ---
def main():
    print(f"Monitoring wallet: {WALLET_ADDRESS}\n")

    wallet_data = get_wallet_data(WALLET_ADDRESS)
    prices = get_token_prices()

    total_value = 0

    for token, amount in wallet_data.items():
        price = prices.get(token, 0)
        value = amount * price
        total_value += value

        message = f"{token}: {amount} → ${value:.2f}"
        send_alert(message)

        threshold = get_threshold(token)
        if threshold and value < threshold:
            send_alert(f"⚠️ {token} value dropped below ${threshold:.2f} → ${value:.2f}")

    send_alert(f"\n💰 Total Wallet Value: ${total_value:.2f}")

if __name__ == "__main__":
    main()