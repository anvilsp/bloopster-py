import requests, json, bsky
# When run, this script will load notifications, check the 50 most recent, reply to any that mention or have replied to the bot, and mark notifications as read.

# bsky auth session
session = bsky.bsky_connect()

get_notifs = requests.get("https://bsky.social/xrpc/app.bsky.notification.listNotifications",
                     headers={"Authorization": "Bearer " + session["accessJwt"]}).json()

#print(len(get_notifs['notifications']))

# request poopster
def get_poopster(seed : str = "") -> str:
    smb_response = requests.get("https://anvilsp.com/poopster/poops.php", params={"input": seed, "parse": "web"})
    stage = smb_response.json()
    return stage

def get_notifications():
    replies = []
    mentions = []

    # request notifications
    notif_json = requests.get("https://bsky.social/xrpc/app.bsky.notification.listNotifications",
                     headers={"Authorization": "Bearer " + session["accessJwt"]}).json()
    notifs = notif_json['notifications'][:50]
    # get notifications that fit our criteria
    for item in notifs:
        if (item['reason'] != "reply" and item['reason'] != "mention") or item['isRead'] == True:
            continue
        if item['reason'] == "reply":
            replies.append(item)
        elif item['reason'] == "mention":
            mentions.append(item)

    # mark notifications as read
    read = requests.post("https://bsky.social/xrpc/app.bsky.notification.updateSeen",
                     headers={"Authorization": "Bearer " + session["accessJwt"]},
                     json = {
                         "seenAt": bsky.now
                     })
    read.raise_for_status()

    # return separated arrays
    return {"replies": replies, "mentions": mentions}

# fetch notifs
notifications = get_notifications()
notif_replies = notifications['replies']
notif_mentions = notifications['mentions']

handle = "@" + bsky.BLUESKY_HANDLE

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
    post = bsky.create_reply(final_reply_text, reply_uri, reply_cid, root_uri, root_cid)
    resp = requests.post("https://bsky.social/xrpc/com.atproto.repo.createRecord",
                     headers={"Authorization": "Bearer " + session["accessJwt"]},
                   json = {
                       "repo": session["did"],
                       "collection": "app.bsky.feed.post",
                       "record": post,
                   })
    print(json.dumps(resp.json(), indent=2))
    resp.raise_for_status()

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

    # for later: check if reply is "-context" and respond with the context of the previous message
    # if ppl *really* don't want to put in the extra work to go to the site and punch in the seed themselves
    
    # if reply is context
        # get parent of reply
        # get parent of parent and its text
        # generate poopster WITH context strings
        # send reply
        # continue

    # check if this reply is a part of a thread chain; this is only true if the mention is in a reply
    if "reply" in mention['record']:
        # data of thread root
        root_uri = mention['record']['reply']['root']['uri']
        root_cid = mention['record']['reply']['root']['cid']

        # reply with root set to thread root
        post = bsky.create_reply(final_reply_text, mention_uri, mention_cid, root_uri, root_cid)
    else:
        # post is not a reply, use self_reply function
        post = bsky.create_self_reply(final_reply_text, mention_uri, mention_cid)

    resp = requests.post("https://bsky.social/xrpc/com.atproto.repo.createRecord",
                     headers={"Authorization": "Bearer " + session["accessJwt"]},
                   json = {
                       "repo": session["did"],
                       "collection": "app.bsky.feed.post",
                       "record": post,
                   })
    print(json.dumps(resp.json(), indent=2))
    resp.raise_for_status()