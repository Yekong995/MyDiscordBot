import requests
from environs import Env


def get_token() -> str:
    env = Env()
    env.read_env()
    return env.str("DISCORD_TOKEN")


def detect_url(message: str):
    env = Env()
    env.read_env()
    apikey = env.str("GOOGLE_SAFE_BROWSING_API_KEY")
    api_url = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
    content_json = {
        "client": {
            "clientId": "OrenBot",
            "clientVersion": "0.0.1"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": message},
            ]
        }
    }
    result = requests.post(api_url, json=(content_json), params={'key': apikey})
    re_json = result.json()
    if re_json == {}:
        return False
    else:
        if "matches" in re_json:
            return True
        else:
            return False
