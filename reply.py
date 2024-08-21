import requests, json, bsky
from os import environ as env
from dotenv import load_dotenv

load_dotenv()

# When run, this script will load notifications, check the 50 most recent, reply to any that mention or have replied to the bot, and mark notifications as read.

# request poopster
def get_poopster(seed : str = "") -> str:
    smb_response = requests.get(env['PARSE_URL'], params={"input": seed, "parse": "web"})
    stage = smb_response.json()
    return stage

# fetch notifs
notif_replies, notif_mentions = bsky.get_notifications(True)

handle = "@" + env['BLUESKY_HANDLE']

# reply to posts from notifs marked as 'reply'
for reply in notif_replies:
    # info of reply itself
    reply_uri = reply['uri']
    reply_cid = reply['cid']

    # reply data
    reply_text = reply['record']['text'].strip()

    # data of thread root
    root_uri = reply['record']['reply']['root']['uri']
    root_cid = reply['record']['reply']['root']['cid']

    # generate a stage, only the stagename variable
    generate_stage = get_poopster(reply_text)
    final_reply_text = generate_stage['stagename']

    # create post
    post = bsky.send_reply(final_reply_text, reply_uri, reply_cid, root_uri, root_cid)
    print(post)

# reply to posts from notifs marked as 'mention'
for mention in notif_mentions:
    # info of mention itself
    mention_uri = mention['uri']
    mention_cid = mention['cid']

    # mention data
    mention_text = mention['record']['text'].strip()
    if mention_text.startswith(handle):
        # if the handle is found at the start, remove it from the string (user wants the pure seed); if it's anywhere but the beginning it's part of the seed
        mention_text = mention_text.replace(handle, '').strip()

    # generate a stage, only the stagename variable
    generate_stage = get_poopster(mention_text)
    final_reply_text = generate_stage['stagename']

    # check if this reply is a part of a thread chain; this is only true if the mention is in a reply
    if "reply" in mention['record']:
        # data of thread root
        root_uri = mention['record']['reply']['root']['uri']
        root_cid = mention['record']['reply']['root']['cid']
        post = bsky.send_reply(final_reply_text, mention_uri, mention_cid, root_uri, root_cid)
    else:
        # post is not a reply, use self_reply function
        post = bsky.send_reply(final_reply_text, mention_uri, mention_cid)
    print(post)