import requests
from datetime import datetime, timezone
from os import environ as env
from dotenv import load_dotenv
from atproto import Client

# Initialize .env file
load_dotenv()

# "now" time for pots
now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

# bsky auth
client = Client(base_url=env['ATPROTO_BASE'])
client.login(env['BLUESKY_HANDLE'], env['BLUESKY_APP_PASSWORD'])

def send_post(text):
    post = client.send_post(text)
    return post

def send_reply(text, uri, cid, root_uri = None, root_cid = None):
    if root_uri == None:
        root_uri = uri
    if root_cid == None:
        root_cid = cid
    
    # create the post with the given parameters
    post = client.send_post(
        text = text,
        reply_to = {
            "root": {
                "uri": root_uri,
                "cid": root_cid
            },
            "parent": {
                "uri": uri,
                "cid": cid
            }
        }
    )
    return post

def mark_as_read():
    # mark notification as read
    client.app.bsky.notification.update_seen(data = {
        "seenAt": client.get_current_time_iso()
    })

def get_notifications(mark_read = False):
    # get the 10 most recent notifications
    notifications = client.app.bsky.notification.list_notifications()['notifications'][:10]

    # lists for replies and mentions
    replies, mentions = [], []

    for notif in notifications:
        # sort unread notifications into two categories: replies and mentions
        if not notif.is_read:
            if notif.reason == "reply":
                replies.append(notif)
            elif notif.reason == "mention":
                mentions.append(notif)
        
    # mark as read if the parameter is set
    if mark_read:
        mark_as_read()
    return replies, mentions