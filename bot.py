import requests, json, bsky
from os import environ as env
from dotenv import load_dotenv
# When run, this script will generate two posts: one containing a stagename and a self-reply to that post containing the context.

# load environment variables
load_dotenv()

# request poopster
def get_poopster(seed : str = "") -> str:
    smb_response = requests.get(env['PARSE_URL'], params={"parse": "web"})
    stage = smb_response.json()
    return stage

stage = get_poopster()

# create post
stage_string = stage['stagename']
post = bsky.send_post(stage_string)
print(post)


context_string = "({first_stage} [{first_context}] + {second_stage} [{second_context}])\nSeed: {seed}".format(
        first_stage = stage['first_stage'], first_context = stage['first_context'],
        second_stage = stage['second_stage'], second_context = stage['second_context'],
        seed = stage['seed'] 
        )

post_uri = post.uri
post_cid = post.cid
reply = bsky.send_reply(
    context_string,
    post_uri,
    post_cid
)
print(reply)