import requests
from typing import Dict, List
from dataclasses import dataclass

NotificationUrlTemplate = "https://twitter.com/i/api/2/notifications/view/{0}.json"


@dataclass
class UserInNotification:
    id_str: str
    screen_name: str
    statuses_count: int


def get_users_in_notification(headers: Dict[str, str], notification_id: str) -> List[UserInNotification]:
    """
    Get a list of user screen names mentioned in a notification
    """
    url = NotificationUrlTemplate.format(notification_id)
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    res = res.json()

    if "globalObjects" not in res:
        raise RuntimeError("No globalObjects in response")
    global_objects = res["globalObjects"]
    if "users" not in global_objects:
        raise RuntimeError("No users in globalObjects")
    users = []
    for _, user in global_objects["users"].items():
        users.append(
            UserInNotification(
                id_str=user["id_str"],
                screen_name=user["screen_name"],
                statuses_count=user["statuses_count"],
            )
        )

    return users
