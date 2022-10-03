import requests
from typing import Dict

SettingsUrl = "https://twitter.com/i/api/1.1/account/settings.json"


def get_my_screen_name(headers: Dict[str, str]) -> str:
    res = requests.get(SettingsUrl, headers=headers)
    res.raise_for_status()
    res = res.json()

    if "screen_name" not in res:
        raise RuntimeError("No screen_name in response")
    return res["screen_name"]
