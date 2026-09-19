FIX V2
Причина ошибки из Railway:
TypeError: Object of type set is not JSON serializable

CLASSES в проекте является Python set. /api/me пытался вернуть его напрямую как JSON.
Исправлено:
- CLASSES -> sorted(list(CLASSES))
- добавлена рекурсивная json_safe() защита API
- панели по рангам и подписанная Mini App сессия сохранены

Установка:
1. Замени bot.py (и лучше miniapp.html тоже) файлами из этого архива.
2. Commit/Push.
3. Railway variables/domain/volume НЕ менять.
4. После Active отправить /app заново и открыть новую кнопку.
