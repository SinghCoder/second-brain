# second-brain
LablabAI Autonomous agents hackathon


## Capture

# For telegram

```bash
curl -X POST https://api.telegram.org/<TELEGRAM_BOT_TOKEN>/setWebhook --data-urlencode "url=<NGROK_URL>/telegram" -d "allowed_updates=[\"message\"]"

curl https://api.telegram.org/<TELEGRAM_BOT_TOKEN>/getWebhookInfo?url=<NGROK_URL>/telegram | jq
```

This would create a webhook for telegram bot.

Now, add the bot to a group, and make sure that while creating the bot, you set the privacy to false. Otherwise, the bot won't be able to see the messages in the group.

Now, you can send a message to the group, and the messages will be received by the bot.

# For Slack

Create a Slack app with following manifest:

```yaml
display_information:
  name: Second-Brain
features:
  bot_user:
    display_name: Second-Brain
    always_online: false
oauth_config:
  scopes:
    user:
      - channels:read
      - groups:read
      - im:history
      - im:read
      - links:read
      - mpim:history
    bot:
      - app_mentions:read
      - channels:history
      - channels:join
      - channels:read
      - channels:write.topic
      - chat:write
      - dnd:read
      - groups:history
      - im:history
      - links:read
      - mpim:history
      - chat:write.customize
      - groups:read
      - im:read
      - im:write
      - mpim:read
      - mpim:write
      - mpim:write.invites
      - usergroups:read
      - users:read
      - users:read.email
settings:
  event_subscriptions:
    request_url: https://822c-45-117-29-250.ngrok.io/slack/events
    user_events:
      - group_open
      - im_created
      - im_open
      - link_shared
      - message.im
      - message.mpim
    bot_events:
      - app_mention
      - channel_archive
      - channel_created
      - channel_deleted
      - channel_rename
      - dnd_updated_user
      - im_history_changed
      - link_shared
      - message.channels
      - message.im
      - message.mpim
  org_deploy_enabled: false
  socket_mode_enabled: false
  token_rotation_enabled: false
```

(Some of the scopes might not be truly needed though).

Now, install the app to your workspace, and invite the bot to a channel. You can then send a message to the channel, and the bot will receive it.

But, make sure, you also Subscribe for events in the workspace, and add the url of the ngrok server with path `/slack/events` as request URL.

# Start

Start the flask app with:

```bash
python3 app.py
```

Start the scheduler with:

```bash
python3 scheduler.py
```

Start ngrok

```bash
ngrok http 3000
```

Register telegram webhook as described above.
Register Slack events as described above.

And, voila! Now you can reproduce the demo.