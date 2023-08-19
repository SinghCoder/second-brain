# second-brain
LablabAI Autonomous agents hackathon


## Capture

# For telegram

curl -X POST https://api.telegram.org/<TELEGRAM_BOT_TOKEN>/setWebhook --data-urlencode "url=<NGROK_URL>/telegram" -d "allowed_updates=[\"message\"]"

curl https://api.telegram.org/<TELEGRAM_BOT_TOKEN>/getWebhookInfo?url=<NGROK_URL>/telegram | jq

This would create a webhook for telegram bot.

Now, add the bot to a group, and make sure that while creating the bot, you set the privacy to false. Otherwise, the bot won't be able to see the messages in the group.

Now, you can send a message to the group, and the messages will be received by the bot.
