import requests, json, bsky
# When run, this script will generate two posts: one containing a stagename and a self-reply to that post containing the context.

# bsky auth session
session = bsky.bsky_connect()

# request poopster
def get_poopster(seed : str = "") -> str:
    smb_response = requests.get('https://anvilsp.com/poopster/poops.php?parse=web')
    stage = smb_response.json()
    return stage

stage = get_poopster()

# create post
stage_string = stage['stagename']
post = bsky.create_post(stage_string)

resp = requests.post("https://bsky.social/xrpc/com.atproto.repo.createRecord",
                     headers={"Authorization": "Bearer " + session["accessJwt"]},
                   json = {
                       "repo": session["did"],
                       "collection": "app.bsky.feed.post",
                       "record": post,
                   })


print(json.dumps(resp.json(), indent=2))
resp.raise_for_status()

post_details = resp.json()


context_string = "({first_stage} [{first_context}] and {second_stage} [{second_context}])".format(
        first_stage = stage['first_stage'], first_context = stage['first_context'],
        second_stage = stage['second_stage'], second_context = stage['second_context'] 
        )

reply = bsky.create_self_reply(context_string, post_details['uri'], post_details['cid'])
resp = requests.post("https://bsky.social/xrpc/com.atproto.repo.createRecord",
                     headers={"Authorization": "Bearer " + session["accessJwt"]},
                   json = {
                       "repo": session["did"],
                       "collection": "app.bsky.feed.post",
                       "record": reply,
                   })


print(json.dumps(resp.json(), indent=2))
resp.raise_for_status()