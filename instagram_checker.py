import os
import logging
from typing import Optional

from dotenv import load_dotenv
from instagrapi import Client

SESSION_FILE = "ig_session.json"

load_dotenv()

IG_USERNAME = os.getenv("IG_USERNAME")
IG_PASSWORD = os.getenv("IG_PASSWORD")

logging.basicConfig(level=logging.INFO, format="%(message)s")


def _login() -> Optional['Client']:
    """Login to Instagram using instagrapi.Client and return the client."""
    if not IG_USERNAME or not IG_PASSWORD:
        logging.error("IG_USERNAME or IG_PASSWORD not provided in .env")
        return None

    client = Client()

    if os.path.exists(SESSION_FILE):
        try:
            client.load_settings(SESSION_FILE)
            client.login(IG_USERNAME, IG_PASSWORD)
            return client
        except Exception as exc:
            logging.warning(f"Failed to reuse session: {exc}")

    try:
        client.login(IG_USERNAME, IG_PASSWORD)
        client.dump_settings(SESSION_FILE)
        return client
    except Exception as exc:
        logging.error(f"Instagram login failed: {exc}")
        return None


def check_unread_messages(limit: int = 5) -> bool:
    """Check Instagram direct messages for unread threads.

    Args:
        limit: Number of recent threads to inspect.

    Returns:
        True if there are unread messages, otherwise False.
    """
    client = _login()
    if not client:
        return False

    try:
        threads = client.direct_threads(amount=limit)
    except Exception as exc:
        logging.error(f"Failed to fetch messages: {exc}")
        return False

    unread_total = 0
    messages_output = []

    for thread in threads:
        if not thread.messages:
            continue
        last_msg = thread.messages[-1]
        user_id = last_msg.user_id
        try:
            username = "@" + client.user_info(user_id).username
        except Exception:
            username = str(user_id)

        text = last_msg.text or ""
        unread = not last_msg.seen
        if unread:
            unread_total += 1
        messages_output.append(
            f"- От {username}: \"{text}\" [{'непрочитано' if unread else 'прочитано'}]"
        )

    if unread_total:
        print(f"Есть {unread_total} непрочитанных сообщений.")
    else:
        print("Непрочитанных сообщений нет.")

    if messages_output:
        print("Последние:")
        for line in messages_output:
            print(line)

    return bool(unread_total)


if __name__ == "__main__":
    check_unread_messages()
