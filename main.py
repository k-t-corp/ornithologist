import logging
import json
import time
import random
from typing import Set
from ornithologist import get_notifications, get_users_in_notification, get_my_screen_name

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def random_wait():
    secs = random.randint(1, 5) + random.random()
    logger.info(f"Waiting {secs} seconds")
    time.sleep(secs)


def main():
    with open('headers.json', 'r') as f:
        headers = json.load(f)

    my_screen_name = get_my_screen_name(headers)
    notifications = get_notifications(headers)
    screen_names = set()  # type: Set[str]
    for notification_id in notifications.ids:
        random_wait()
        users = get_users_in_notification(headers, notification_id)
        for user in users:
            if user.statuses_count != 0 and user.screen_name != my_screen_name:
                screen_names.add(user.screen_name)
    print(screen_names)


if __name__ == '__main__':
    main()
