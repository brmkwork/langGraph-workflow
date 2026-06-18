from datetime import datetime

def log(tag: str, message: str, data: dict = None):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"\n[{timestamp}] {tag}")
    print(f"  {message}")
    if data:
        for key, value in data.items():
            print(f"  {key}: {value}")
    print("  " + "─" * 50)