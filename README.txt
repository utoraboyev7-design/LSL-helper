LSL Helper upgrade

1. Replace your repo bot.py with this bot.py.
2. Put miniapp.html next to bot.py.
3. Replace requirements.txt with this one (or add aiohttp).
4. Push to GitHub and wait for Railway deploy.
5. Railway -> service Settings -> Networking -> Generate Domain.
6. Railway Variables -> WEBAPP_URL = your generated https:// domain (no quotes).
7. Redeploy.
8. In private chat with bot use /app.
9. Optional: BotFather -> /mybots -> your bot -> Bot Settings -> Configure Mini App -> Enable Mini App and set the same HTTPS URL.

Group commands:
- reply /warn reason
- reply /warns
- reply /clearwarns
- reply /mute 30
- reply /unmute
- reply /kick
- reply /ban
- /unban TELEGRAM_ID

Bot must be group admin with Restrict/Ban permissions.
