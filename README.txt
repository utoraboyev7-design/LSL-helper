LSL HELPER PRO — установка

Файлы:
- bot.py
- miniapp.html
- requirements.txt

1) Замени эти файлы в GitHub-репозитории.
2) Railway Variables:
   WEBAPP_URL=https://lsl-helper-production.up.railway.app
   DATA_DIR=/app/data
   BOT_TOKEN=твой токен
   DEVELOPER_PIN=твой PIN
3) Railway: добавь Volume к сервису LSL-helper и mount path поставь /app/data.
   Это обязательно, иначе users/content/groups могут пропасть после redeploy.
4) Deploy.
5) В Telegram открой /app.

Что добавлено:
- профессиональнее Mini App: dashboard, ДЗ, новости, люди, группы;
- ДЗ выбирается из списка классов;
- сохранённое в Mini App ДЗ читается кнопкой ДЗ в боте;
- поиск/фильтр пользователей;
- изменение ролей;
- бан/разбан в самом боте;
- mute/unmute/warn/clearwarns/kick/ban по выбранной группе;
- журнал последних действий;
- Telegram initData проверяется сервером;
- иерархия ролей применяется на backend, а не только в интерфейсе.

Новости оставлены простыми, как просил пользователь.
