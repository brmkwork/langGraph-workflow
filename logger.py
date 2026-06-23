from datetime import datetime

def log(tag: str, message: str, data: dict = None):
    timestamp = datetime.now().strftime("%H:%M:%S")
    data_str = ""
    if data:
        parts = [f"{k}={v}" for k, v in data.items()]
        data_str = " | " + ", ".join(parts)
    print(f"[{timestamp}] {tag}: {message}{data_str}")