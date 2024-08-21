# bloopster.py
A Bluesky bot for creating posts based on generated results from [Poopster](https://github.com/anvilsp/Poopster), integrating the Bluesky and AT Protocol API.

`bot.py` creates two posts: a parent post creating a generated stage name, and a reply post containing the original stage names and the games they originate from.

`reply.py` fetches the unread `mention` and `reply` notifications from the Bluesky user, generates a random stage name based on the text of the notification's associated post, and marks the notifications as read.

## Environment Variables
The `.env` file should be set up as follows:
```
PARSE_URL="https://poopster.anvilsp.com/api"
BLUESKY_HANDLE="YOUR_BSKY_HANDLE_HERE"
BLUESKY_APP_PASSWORD="YOUR_BSKY_APP_PASSWORD_HERE"
ATPROTO_BASE="https://bsky.social"
```