import logging
import requests
from typing import List, Optional, Dict
from dataclasses import dataclass

logger = logging.getLogger(__name__)

NotificationsUrlQueryParams = {
    "include_profile_interstitial_type": 1,
    "include_blocking": 1,
    "include_blocked_by": 1,
    "include_followed_by": 1,
    "include_want_retweets": 1,
    "include_mute_edge": 1,
    "include_can_dm": 1,
    "include_can_media_tag": 1,
    "include_ext_has_nft_avatar": 1,
    "skip_status": 1,
    "cards_platform": "Web-12",
    "include_cards": 1,
    "include_ext_alt_text": "true",
    "include_ext_limited_action_results": "false",
    "include_quote_count": "true",
    "include_reply_count": 1,
    "tweet_mode": "extended",
    "include_ext_collab_control": "true",
    "include_entities": "true",
    "include_user_entities": "true",
    "include_ext_media_color": "true",
    "include_ext_media_availability": "true",
    "include_ext_sensitive_media_warning": "true",
    "include_ext_trusted_friends_metadata": "true",
    "send_error_codes": "true",
    "simple_quoted_tweet": "true",
    "count": 20,
    "ext": "mediaStats,highlightedLabel,hasNftAvatar,voiceInfo,enrichments,superFollowMetadata,unmentionInfo,editControl,collab_control,vibe",
}
NotificationsUrl = "https://twitter.com/i/api/2/notifications/all.json"


@dataclass
class Notifications:
    ids: List[str]
    next_cursor: Optional[str]
    earliest_timestamp_ms: int


def get_notifications(headers: Dict[str, str], next_cursor: Optional[str] = None) -> Notifications:
    """
    Get a list of IDs for individual notification, next cursor and timestamp for the earliest notification

    :param headers:
    :return:
    """
    query_params = NotificationsUrlQueryParams.copy()
    if next_cursor:
        query_params["cursor"] = next_cursor
    res = requests.get(NotificationsUrl, headers=headers, params=query_params)
    res.raise_for_status()
    res = res.json()

    if "timeline" not in res:
        raise RuntimeError("No timeline in response")
    timeline = res["timeline"]
    if "instructions" not in timeline:
        raise RuntimeError("No instructions in timeline")
    instructions = timeline["instructions"]
    add_entries = None
    for instruction in instructions:
        if "addEntries" in instruction:
            add_entries = instruction["addEntries"]
            break
    if not add_entries:
        raise RuntimeError("No addEntries in instructions")
    if "entries" not in add_entries:
        raise RuntimeError("No entries in addEntries")
    entries = add_entries["entries"]

    ids = []
    next_cursor = None
    warnings = {}  # type: Dict[str, List[str]]
    for entry in entries:
        if "entryId" not in entry:
            raise RuntimeError("No entryId in entry")
        entry_id = entry["entryId"]

        def warning(msg):
            if entry_id not in warnings:
                warnings[entry_id] = []
            warnings[entry_id].append(msg)

        if "content" not in entry:
            warning("No content in entry")
            continue
        content = entry["content"]
        if "item" not in content:
            if "operation" not in content:
                warning("No item or operation in content")
                continue
            operation = content["operation"]
            if "cursor" not in operation:
                warning("No cursor in operation")
                continue
            cursor = operation["cursor"]
            if "cursorType" not in cursor:
                warning("No cursorType in cursor")
                continue
            cursor_type = cursor["cursorType"]
            if cursor_type == "Bottom":
                next_cursor = cursor["value"]
                continue
        else:
            item = content["item"]
            if "content" not in item:
                warning("No content in item")
                continue
            item_content = item["content"]
            if "notification" not in item_content:
                warning("No notification in item content")
                continue
            notification = item_content["notification"]
            if "id" not in notification:
                warning("No id in notification")
                continue
            ids.append(notification["id"])

    if warnings:
        logger.warning("There were warnings! They are:")
        logger.warning(warnings)

    earliest_timestamp_ms = 0
    if "globalObjects" not in res:
        raise RuntimeError("No globalObjects in response")
    global_objects = res["globalObjects"]
    if "notifications" not in global_objects:
        raise RuntimeError("No notifications in globalObjects")
    notifications = global_objects["notifications"]
    for _, notification in notifications.items():
        if "timestampMs" not in notification:
            continue
        timestamp_ms = int(notification["timestampMs"])
        if earliest_timestamp_ms == 0 or timestamp_ms < earliest_timestamp_ms:
            earliest_timestamp_ms = timestamp_ms

    return Notifications(
        ids=ids,
        next_cursor=next_cursor,
        earliest_timestamp_ms=earliest_timestamp_ms
    )
