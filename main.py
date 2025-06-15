import time
from utils.instagram_checker import check_instagram

if __name__ == "__main__":
    while True:
        try:
            check_instagram()
        except Exception as exc:
            print(f"Error during check: {exc}")
        time.sleep(300)

