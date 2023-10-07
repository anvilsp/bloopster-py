import requests
from datetime import datetime, timezone

BLUESKY_HANDLE = "INSERT_HANDLE_HERE"
BLUESKY_APP_PASSWORD = "INSERT_APP_PW_HERE"

# "now" time for pots
now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

# bsky auth
def bsky_connect(raw : bool = False):
    resp = requests.post("https://bsky.social/xrpc/com.atproto.server.createSession", json={"identifier": BLUESKY_HANDLE, "password": BLUESKY_APP_PASSWORD})
    resp.raise_for_status()
    session = resp.json()
    if raw:
        return resp
    else:
        return session

# function to create a post
def create_post(text : str):
    post = {
        "$type": "app.bsky.feed.post",
        "text": text,
        "createdAt": now,
        "langs": {"en-US"}
        }
    return post

# function to a reply to a post that is part of a chain
def create_reply(text : str, uri : str, cid: str, root_uri : str, root_cid : str):
    post = {
        "$type": "app.bsky.feed.post",
        "text": text,
        "createdAt": now,
        "langs": {"en-US"},
        "reply": {
            "root": {
                "uri": root_uri,
                "cid": root_cid
            },
            "parent": {
                "uri": uri,
                "cid": cid
            }
        }
    }
    return post

# function to create a reply to a post that is not part of a chain
def create_self_reply(text : str, uri : str, cid : str):
    post = {
        "$type": "app.bsky.feed.post",
        "text": text,
        "createdAt": now,
        "langs": {"en-US"},
        "reply": {
            "root": {
                "uri": uri,
                "cid": cid
            },
            "parent": {
                "uri": uri,
                "cid": cid
            }
        }
    }
    return post