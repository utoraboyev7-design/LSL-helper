import asyncio
import json
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,
                           InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery,
                           ChatMemberUpdated, ChatPermissions)

from languages.ru.texts import TEXTS as RU_TEXTS
from languages.ru.subjects import SUBJECTS as RU_SUBJECTS

from languages.uz.texts import TEXTS as UZ_TEXTS
from languages.uz.subjects import SUBJECTS as UZ_SUBJECTS

from languages.en.texts import TEXTS as EN_TEXTS
from languages.en.subjects import SUBJECTS as EN_SUBJECTS


# ============================================================
# НАСТРОЙКИ
# ============================================================



BOT_TOKEN = os.getenv("BOT_TOKEN")
DEVELOPER_PIN = os.getenv("DEVELOPER_PIN")

DATA_FILE = "users.json"
GROUPS_FILE = "groups.json"

dp = Dispatcher()

# ============================================================
# ЯЗЫКИ
# ============================================================

LANGUAGES = {
    "🇷🇺 Русский": "ru",
    "🇺🇿 O‘zbekcha": "uz",
    "🇬🇧 English": "en",
}

TEXTS = {
    "ru": RU_TEXTS,
    "uz": UZ_TEXTS,
    "en": EN_TEXTS,
}

SUBJECTS = {
    "ru": RU_SUBJECTS,
    "uz": UZ_SUBJECTS,
    "en": EN_SUBJECTS,
}


# ============================================================
# КЛАССЫ
# ============================================================

CLASSES = {
    "1А", "1Б",
    "2А", "2Б",
    "3А", "3Б",
    "4А", "4Б",
    "5А", "5Б",
    "6А", "6Б",
    "7А", "7Б",
    "8А",
    "9А", "9Б",
    "10А", "10Б",
    "11А"
}


# ============================================================
# РАСПИСАНИЕ
# ============================================================

SCHEDULES = {

    "6Б": {
        "Понедельник": [
            ("8:30–9:15", "Informatika"),
            ("9:25–10:10", "Informatika"),
            ("10:20–11:05", "Tasviriy san'at"),
            ("11:15–12:00", "Nutq madaniyati"),
            ("13:00–13:45", "Adabiyot"),
            ("13:55–14:40", "Tarix"),
            ("14:50–15:35", "Matematika"),
            ("15:45–16:30", "Matematika"),
        ],
        "Вторник": [
            ("8:30–9:15", "Ona tili"),
            ("9:25–10:10", "Nutq madaniyati"),
            ("10:20–11:05", "Science"),
            ("11:15–12:00", "Adabiyot"),
            ("13:00–13:45", "Texnologiya"),
            ("13:55–14:40", "Texnologiya"),
            ("14:50–15:35", "Chet tili"),
            ("15:45–16:30", "Chet tili"),
        ],
        "Среда": [
            ("8:30–9:15", "Mat. kurs"),
            ("9:25–10:10", "Mat. kurs"),
            ("10:20–11:05", "Ona tili"),
            ("11:15–12:00", "Tarbiya"),
            ("13:00–13:45", "Chet tili"),
            ("13:55–14:40", "Chet tili"),
            ("14:50–15:35", "Rus tili"),
            ("15:45–16:30", "Tarix"),
        ],
        "Четверг": [
            ("8:30–9:15", "Matematika"),
            ("9:25–10:10", "Matematika"),
            ("10:20–11:05", "Ona tili"),
            ("11:15–12:00", "Science"),
            ("13:00–13:45", "Nutq madaniyati"),
            ("13:55–14:40", "Rus tili"),
            ("14:50–15:35", "Informatika"),
            ("15:45–16:30", "Informatika"),
        ],
        "Пятница": [
            ("8:30–9:15", "Ona tili"),
            ("9:25–10:10", "Chet tili"),
            ("10:20–11:05", "Chet tili"),
            ("11:15–12:00", "Science"),
            ("13:00–13:45", "Sinf soati"),
            ("13:55–14:40", "Musiqa"),
            ("14:50–15:35", "Chet tili"),
            ("15:45–16:30", "Chet tili"),
        ],
        "Суббота": [
            ("8:30–9:15", "Jis/tar"),
            ("9:25–10:10", "Jis/tar"),
            ("10:20–11:05", "Informatika"),
            ("11:15–12:00", "Informatika"),
            ("13:00–13:45", "Chet tili"),
            ("13:55–14:40", "Chet tili"),
            ("14:50–15:35", "Matematika"),
            ("15:45–16:30", "Matematika"),
        ],
    },

    "7А": {
        "Понедельник": [
            ("8:30–9:15", "Informatika"),
            ("9:25–10:10", "Informatika"),
            ("10:20–11:05", "Ona tili"),
            ("11:15–12:00", "Tarbiya"),
            ("13:00–13:45", "Chet tili"),
            ("13:55–14:40", "Chet tili"),
            ("14:50–15:35", "Geografiya"),
            ("15:45–16:30", "Rus tili"),
        ],
        "Вторник": [
            ("8:30–9:15", "Kimyo"),
            ("9:25–10:10", "Chet tili"),
            ("10:20–11:05", "Chet tili"),
            ("11:15–12:00", "Mat. kurs"),
            ("13:00–13:45", "Mat. kurs"),
            ("13:55–14:40", "Tarix"),
            ("14:50–15:35", "Geografiya"),
            ("15:45–16:30", "Matematika"),
        ],
        "Среда": [
            ("8:30–9:15", "Chet tili"),
            ("9:25–10:10", "Chet tili"),
            ("10:20–11:05", "Adabiyot"),
            ("11:15–12:00", "Biologiya"),
            ("13:00–13:45", "Informatika"),
            ("13:55–14:40", "Informatika"),
            ("14:50–15:35", "Matematika"),
            ("15:45–16:30", "Matematika"),
        ],
        "Четверг": [
            ("8:30–9:15", "Biologiya"),
            ("9:25–10:10", "Ona tili"),
            ("10:20–11:05", "Fizika"),
            ("11:15–12:00", "Adabiyot"),
            ("13:00–13:45", "Jis/tar"),
            ("13:55–14:40", "Jis/tar"),
            ("14:50–15:35", "Chet tili"),
            ("15:45–16:30", "Chet tili"),
        ],
        "Пятница": [
            ("8:30–9:15", "Informatika"),
            ("9:25–10:10", "Informatika"),
            ("10:20–11:05", "Fizika"),
            ("11:15–12:00", "Rus tili"),
            ("13:00–13:45", "Sinf soati"),
            ("13:55–14:40", "Tarix"),
            ("14:50–15:35", "Texnologiya"),
            ("15:45–16:30", "Texnologiya"),
        ],
        "Суббота": [
            ("8:30–9:15", "Tarix"),
            ("9:25–10:10", "Chet tili"),
            ("10:20–11:05", "Chet tili"),
            ("11:15–12:00", "Kimyo"),
            ("13:00–13:45", "Matematika"),
            ("13:55–14:40", "Matematika"),
            ("14:50–15:35", "Ona tili"),
            ("15:45–16:30", "Chizmachilik / Musiqa"),
        ],
    },

    "8А": {
        "Понедельник": [
            ("8:30–9:15", "Adabiyot"),
            ("9:25–10:10", "Geografiya"),
            ("10:20–11:05", "Algebra"),
            ("11:15–12:00", "Geometriya"),
            ("13:00–13:45", "Informatika"),
            ("13:55–14:40", "Informatika"),
            ("14:50–15:35", "Chet tili"),
            ("15:45–16:30", "Chet tili"),
        ],
        "Вторник": [
            ("8:30–9:15", "Adabiyot"),
            ("9:25–10:10", "Algebra"),
            ("10:20–11:05", "Geometriya"),
            ("11:15–12:00", "Kimyo"),
            ("13:00–13:45", "Chet tili"),
            ("13:55–14:40", "Chet tili"),
            ("14:50–15:35", "Ona tili"),
            ("15:45–16:30", "Iqtisod / Geografiya"),
        ],
        "Среда": [
            ("8:30–9:15", "Informatika"),
            ("9:25–10:10", "Informatika"),
            ("10:20–11:05", "Tarbiya"),
            ("11:15–12:00", "Mat. kurs"),
            ("13:00–13:45", "Mat. kurs"),
            ("13:55–14:40", "Huquq"),
            ("14:50–15:35", "Chet tili"),
            ("15:45–16:30", "Chet tili"),
        ],
        "Четверг": [
            ("8:30–9:15", "Chet tili"),
            ("9:25–10:10", "Chet tili"),
            ("10:20–11:05", "Kimyo"),
            ("11:15–12:00", "Chet tili"),
            ("13:00–13:45", "Chet tili"),
            ("13:55–14:40", "Ona tili"),
            ("14:50–15:35", "Chizmachilik / Tarix"),
            ("15:45–16:30", "Texnologiya"),
        ],
        "Пятница": [
            ("8:30–9:15", "Rus tili"),
            ("9:25–10:10", "Fizika"),
            ("10:20–11:05", "Algebra"),
            ("11:15–12:00", "Tarix"),
            ("13:00–13:45", "Sinf soati"),
            ("13:55–14:40", "Fizika"),
            ("14:50–15:35", "Biologiya"),
            ("15:45–16:30", "Algebra"),
        ],
        "Суббота": [
            ("8:30–9:15", "Informatika"),
            ("9:25–10:10", "Informatika"),
            ("10:20–11:05", "Rus tili"),
            ("11:15–12:00", "Tarix"),
            ("13:00–13:45", "Ona tili"),
            ("13:55–14:40", "Biologiya"),
            ("14:50–15:35", "Jis/tar"),
            ("15:45–16:30", "Jis/tar"),
        ],
    },
}


# ============================================================
# ДНИ НЕДЕЛИ
# ============================================================

DAY_NAMES = {
    "ru": {
        "Понедельник": "Понедельник",
        "Вторник": "Вторник",
        "Среда": "Среда",
        "Четверг": "Четверг",
        "Пятница": "Пятница",
        "Суббота": "Суббота",
    },

    "uz": {
        "Понедельник": "Dushanba",
        "Вторник": "Seshanba",
        "Среда": "Chorshanba",
        "Четверг": "Payshanba",
        "Пятница": "Juma",
        "Суббота": "Shanba",
    },

    "en": {
        "Понедельник": "Monday",
        "Вторник": "Tuesday",
        "Среда": "Wednesday",
        "Четверг": "Thursday",
        "Пятница": "Friday",
        "Суббота": "Saturday",
    },
}


# ============================================================
# РАБОТА С ПОЛЬЗОВАТЕЛЯМИ
# ============================================================

def load_users():
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


users = load_users()


def save_users():
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=4)


def create_user(user_id, tg_user=None):
    user_id = str(user_id)

    if user_id not in users:
        users[user_id] = {
            "language": None,
            "class": None,
            "role": "student",
            "banned": False,
            "username": None,
            "first_name": None,
            "last_name": None
        }

    user = users[user_id]
    user.setdefault("language", None)
    user.setdefault("class", None)
    user.setdefault("role", "student")
    user.setdefault("banned", False)
    user.setdefault("username", None)
    user.setdefault("first_name", None)
    user.setdefault("last_name", None)
    user.setdefault("role", "student")
    user.setdefault("banned", False)

    if tg_user is not None:
        user["username"] = tg_user.username
        user["first_name"] = tg_user.first_name
        user["last_name"] = tg_user.last_name

    save_users()


def get_language(user_id):
    user = users.get(str(user_id), {})
    language = user.get("language")
    if language in TEXTS:
        return language
    return None


def get_class(user_id):
    return users.get(str(user_id), {}).get("class")


def get_role(user_id):
    return users.get(str(user_id), {}).get("role", "student")


def is_banned(user_id):
    return users.get(str(user_id), {}).get("banned", False)


def is_developer(user_id):
    return get_role(user_id) == "developer"


# ============================================================
# МЕНЮ ЯЗЫКА
# ============================================================

language_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇷🇺 Русский")],
        [KeyboardButton(text="🇺🇿 O‘zbekcha")],
        [KeyboardButton(text="🇬🇧 English")],
    ],
    resize_keyboard=True
)


# ============================================================
# МЕНЮ КЛАССОВ
# ============================================================

class_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="1А"), KeyboardButton(text="1Б")],
        [KeyboardButton(text="2А"), KeyboardButton(text="2Б")],
        [KeyboardButton(text="3А"), KeyboardButton(text="3Б")],
        [KeyboardButton(text="4А"), KeyboardButton(text="4Б")],
        [KeyboardButton(text="5А"), KeyboardButton(text="5Б")],
        [KeyboardButton(text="6А"), KeyboardButton(text="6Б")],
        [KeyboardButton(text="7А"), KeyboardButton(text="7Б")],
        [KeyboardButton(text="8А")],
        [KeyboardButton(text="9А"), KeyboardButton(text="9Б")],
        [KeyboardButton(text="10А"), KeyboardButton(text="10Б")],
        [KeyboardButton(text="11А")],
    ],
    resize_keyboard=True
)


# ============================================================
# ГЛАВНОЕ МЕНЮ
# ============================================================

def main_menu(user_id):

    language = get_language(user_id)
    class_name = get_class(user_id)

    t = TEXTS[language]

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=t["schedule"]),
                KeyboardButton(text=t["books"]),
            ],
            [
                KeyboardButton(text=t["homework"]),
                KeyboardButton(text=t["news"]),
            ],
            [
                KeyboardButton(text=t["contacts"]),
                KeyboardButton(text=t["help"]),
            ],
            [
                KeyboardButton(
                    text=t["change_class"].format(
                        class_name=class_name
                    )
                )
            ],
            [
                KeyboardButton(text=t["language"])
            ],
        ],
        resize_keyboard=True
    )


# ============================================================
# РЕЖИМ РАЗРАБОТЧИКА
# ============================================================

class DeveloperLogin(StatesGroup):
    waiting_for_pin = State()

class DeveloperAction(StatesGroup):
    waiting_for_user = State()

ROLE_LABELS = {
    "student": "Пользователь",
    "junior_moder": "Мл. модер",
    "moder": "Модер",
    "junior_admin": "Мл. админ",
    "admin": "Админ",
    "zga": "ЗГА",
    "ga": "ГА",
    "creator": "Создатель",
    "teacher": "Учитель",
    "developer": "Разработчик",
}

ROLE_LEVELS = {
    "student": 0,
    "teacher": 10,
    "junior_moder": 20,
    "moder": 30,
    "junior_admin": 40,
    "admin": 50,
    "zga": 60,
    "ga": 70,
    "creator": 100,
    "developer": 110,
}

def role_label(role):
    return ROLE_LABELS.get(role, role)

def load_groups():
    if not os.path.exists(GROUPS_FILE):
        return {}
    try:
        with open(GROUPS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}

groups = load_groups()

def save_groups():
    with open(GROUPS_FILE, "w", encoding="utf-8") as f:
        json.dump(groups, f, ensure_ascii=False, indent=4)

def remember_group(chat):
    if chat.type not in {"group", "supergroup"}:
        return
    groups[str(chat.id)] = {
        "title": chat.title or "Без названия",
        "username": chat.username,
        "type": chat.type,
        "active": True,
    }
    save_groups()

developer_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👥 Пользователи"), KeyboardButton(text="📊 Статистика")],
        [KeyboardButton(text="🏫 Группы"), KeyboardButton(text="🛡 Персонал")],
        [KeyboardButton(text="🔎 Найти пользователя")],
        [KeyboardButton(text="🚪 Выйти из панели")]
    ],
    resize_keyboard=True
)

def developer_user_card(user_id, user):
    username = f"@{user.get('username')}" if user.get("username") else "—"
    full_name = " ".join(
        part for part in [user.get("first_name"), user.get("last_name")] if part
    ) or "—"
    return (
        f"👤 {full_name}\n"
        f"🆔 {user_id}\n"
        f"🔗 {username}\n"
        f"🎓 Класс: {user.get('class') or '—'}\n"
        f"🌐 Язык: {user.get('language') or '—'}\n"
        f"🛡 Должность: {role_label(user.get('role', 'student'))}\n"
        f"🚫 Бан: {'да' if user.get('banned', False) else 'нет'}"
    )

def user_manage_keyboard(user_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎖 Изменить должность", callback_data=f"roles:{user_id}")],
        [InlineKeyboardButton(
            text="✅ Разбанить" if users.get(str(user_id), {}).get("banned") else "🚫 Заблокировать",
            callback_data=f"ban:{user_id}"
        )]
    ])

def role_keyboard(user_id):
    rows = []
    role_ids = ["student", "junior_moder", "moder", "junior_admin", "admin", "zga", "ga", "teacher"]
    for i in range(0, len(role_ids), 2):
        row = [
            InlineKeyboardButton(
                text=ROLE_LABELS[r],
                callback_data=f"setrole:{user_id}:{r}"
            )
            for r in role_ids[i:i+2]
        ]
        rows.append(row)
    # Creator is intentionally separate/protected.
    rows.append([InlineKeyboardButton(text="👑 Создатель", callback_data=f"setrole:{user_id}:creator")])
    rows.append([InlineKeyboardButton(text="⬅️ Назад", callback_data=f"user:{user_id}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def can_manage(actor_id, target_id, new_role=None):
    actor = users.get(str(actor_id), {})
    target = users.get(str(target_id), {})
    actor_role = actor.get("role", "student")
    target_role = target.get("role", "student")

    if actor_role == "developer":
        return True
    if actor_role != "creator":
        return False
    if target_role == "developer":
        return False
    if new_role == "developer":
        return False
    return True


# ============================================================
# МОДЕРАЦИЯ В ГРУППАХ ПО РОЛЯМ
# ============================================================

GROUP_MOD_ROLES = {
    "junior_moder", "moder", "junior_admin", "admin",
    "zga", "ga", "creator", "developer"
}

def can_group_moderate(actor_id, target_id):
    """Сотрудник может модерировать только пользователя с ролью ниже своей."""
    actor_role = get_role(actor_id)
    target_role = get_role(target_id)

    if actor_role not in GROUP_MOD_ROLES:
        return False

    return ROLE_LEVELS.get(actor_role, 0) > ROLE_LEVELS.get(target_role, 0)

def parse_mute_minutes(text):
    # /mute -> 10 минут по умолчанию
    # /mute 30 -> 30 минут
    parts = (text or "").split()
    if len(parts) < 2:
        return 10
    try:
        minutes = int(parts[1])
        return max(1, min(minutes, 10080))  # максимум 7 дней
    except ValueError:
        return None

@dp.message(Command("mute"))
async def group_mute(message: Message, bot: Bot):
    if message.chat.type not in {"group", "supergroup"}:
        return

    remember_group(message.chat)
    create_user(message.from_user.id, message.from_user)

    if get_role(message.from_user.id) not in GROUP_MOD_ROLES:
        return

    if not message.reply_to_message or not message.reply_to_message.from_user:
        await message.reply("⚠️ Ответь командой /mute на сообщение пользователя.")
        return

    target = message.reply_to_message.from_user
    create_user(target.id, target)

    if target.id == message.from_user.id:
        await message.reply("⚠️ Себя замутить нельзя.")
        return

    if not can_group_moderate(message.from_user.id, target.id):
        await message.reply("⛔ Нельзя мутить пользователя с такой же или более высокой должностью.")
        return

    minutes = parse_mute_minutes(message.text)
    if minutes is None:
        await message.reply("⚠️ Формат: /mute 10 — мут на 10 минут.")
        return

    from datetime import datetime, timedelta, timezone
    until = datetime.now(timezone.utc) + timedelta(minutes=minutes)

    try:
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=target.id,
            permissions=ChatPermissions(
                can_send_messages=False,
                can_send_audios=False,
                can_send_documents=False,
                can_send_photos=False,
                can_send_videos=False,
                can_send_video_notes=False,
                can_send_voice_notes=False,
                can_send_polls=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False,
                can_change_info=False,
                can_invite_users=False,
                can_pin_messages=False,
                can_manage_topics=False,
            ),
            until_date=until
        )
        name = f"@{target.username}" if target.username else target.full_name
        await message.reply(f"🔇 {name} получил мут на {minutes} мин.\n🛡 Выдал: {role_label(get_role(message.from_user.id))}")
    except Exception:
        await message.reply(
            "❌ Не получилось выдать мут.\n"
            "Проверь, что бот — администратор группы и у него есть право ограничивать участников."
        )

@dp.message(Command("unmute"))
async def group_unmute(message: Message, bot: Bot):
    if message.chat.type not in {"group", "supergroup"}:
        return

    remember_group(message.chat)
    create_user(message.from_user.id, message.from_user)

    if get_role(message.from_user.id) not in GROUP_MOD_ROLES:
        return

    if not message.reply_to_message or not message.reply_to_message.from_user:
        await message.reply("⚠️ Ответь командой /unmute на сообщение пользователя.")
        return

    target = message.reply_to_message.from_user
    create_user(target.id, target)

    if not can_group_moderate(message.from_user.id, target.id):
        await message.reply("⛔ Нельзя размутить пользователя с такой же или более высокой должностью.")
        return

    try:
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=target.id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_audios=True,
                can_send_documents=True,
                can_send_photos=True,
                can_send_videos=True,
                can_send_video_notes=True,
                can_send_voice_notes=True,
                can_send_polls=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_change_info=False,
                can_invite_users=True,
                can_pin_messages=False,
                can_manage_topics=False,
            )
        )
        name = f"@{target.username}" if target.username else target.full_name
        await message.reply(f"🔊 Мут снят с {name}.")
    except Exception:
        await message.reply(
            "❌ Не получилось снять мут.\n"
            "Проверь права администратора у бота."
        )

@dp.my_chat_member()
async def bot_membership_changed(event: ChatMemberUpdated):
    chat = event.chat
    if chat.type not in {"group", "supergroup"}:
        return
    new_status = event.new_chat_member.status
    groups[str(chat.id)] = {
        "title": chat.title or "Без названия",
        "username": chat.username,
        "type": chat.type,
        "active": new_status not in {"left", "kicked"},
    }
    save_groups()

@dp.message(Command("panel"))
async def open_panel(message: Message, state: FSMContext):
    user_id = message.from_user.id
    create_user(user_id, message.from_user)

    if is_banned(user_id):
        await message.answer("🚫 Доступ к боту для вашего аккаунта заблокирован.")
        return

    if is_developer(user_id) or get_role(user_id) == "creator":
        await message.answer("👑 Панель управления", reply_markup=developer_menu)
        return

    if not DEVELOPER_PIN:
        await message.answer("⚠️ DEVELOPER_PIN не настроен на сервере.")
        return

    await state.set_state(DeveloperLogin.waiting_for_pin)
    await message.answer("🔐 Введите PIN разработчика:", reply_markup=ReplyKeyboardRemove())

@dp.message(DeveloperLogin.waiting_for_pin)
async def developer_pin_login(message: Message, state: FSMContext):
    if message.text == DEVELOPER_PIN:
        user_id = str(message.from_user.id)
        create_user(user_id, message.from_user)
        users[user_id]["role"] = "developer"
        save_users()
        await state.clear()
        await message.answer("✅ Доступ подтверждён.\n\n👑 Режим разработчика", reply_markup=developer_menu)
        return
    await message.answer("❌ Неверный PIN. Попробуйте ещё раз или отправьте /start для выхода.")

@dp.message(F.text == "📊 Статистика")
async def developer_stats(message: Message):
    if get_role(message.from_user.id) not in {"developer", "creator"}:
        return
    total = len(users)
    banned = sum(1 for u in users.values() if u.get("banned", False))
    staff = sum(1 for u in users.values() if u.get("role", "student") != "student")
    active_groups = sum(1 for g in groups.values() if g.get("active", True))
    await message.answer(
        "📊 Статистика бота\n\n"
        f"👥 Пользователей: {total}\n"
        f"🛡 Персонала: {staff}\n"
        f"🏫 Групп: {active_groups}\n"
        f"🚫 Заблокировано: {banned}"
    )

@dp.message(F.text == "👥 Пользователи")
async def developer_users(message: Message):
    if get_role(message.from_user.id) not in {"developer", "creator"}:
        return
    if not users:
        await message.answer("Пользователей пока нет.")
        return
    await message.answer(f"👥 Всего пользователей: {len(users)}")
    for user_id, user in list(users.items())[:20]:
        await message.answer(developer_user_card(user_id, user), reply_markup=user_manage_keyboard(user_id))
    if len(users) > 20:
        await message.answer("ℹ️ Пока показаны первые 20 пользователей.")

@dp.message(F.text == "🔎 Найти пользователя")
async def find_user_start(message: Message, state: FSMContext):
    if get_role(message.from_user.id) not in {"developer", "creator"}:
        return
    await state.set_state(DeveloperAction.waiting_for_user)
    await message.answer("🔎 Отправь Telegram ID или @username пользователя:", reply_markup=ReplyKeyboardRemove())

@dp.message(DeveloperAction.waiting_for_user)
async def find_user_finish(message: Message, state: FSMContext):
    if get_role(message.from_user.id) not in {"developer", "creator"}:
        await state.clear()
        return
    query = (message.text or "").strip()
    found_id = None
    if query.isdigit() and query in users:
        found_id = query
    else:
        username = query.lstrip("@").lower()
        for uid, u in users.items():
            if (u.get("username") or "").lower() == username:
                found_id = uid
                break
    await state.clear()
    if not found_id:
        await message.answer("❌ Пользователь не найден.", reply_markup=developer_menu)
        return
    await message.answer(
        developer_user_card(found_id, users[found_id]),
        reply_markup=user_manage_keyboard(found_id)
    )
    await message.answer("👑 Панель управления", reply_markup=developer_menu)

@dp.message(F.text == "🏫 Группы")
async def developer_groups(message: Message):
    if get_role(message.from_user.id) not in {"developer", "creator"}:
        return
    active = [(gid, g) for gid, g in groups.items() if g.get("active", True)]
    if not active:
        await message.answer(
            "🏫 Пока групп нет в базе.\n\n"
            "Добавь бота в группу (или пере-добавь его), и Telegram пришлёт событие — группа появится здесь."
        )
        return
    text = [f"🏫 Группы бота: {len(active)}\n"]
    for gid, g in active[:30]:
        uname = f"@{g['username']}" if g.get("username") else "без username"
        text.append(f"• {g.get('title', 'Без названия')}\n  🆔 {gid} | {uname}")
    await message.answer("\n".join(text))

@dp.message(F.text == "🛡 Персонал")
async def developer_staff(message: Message):
    if get_role(message.from_user.id) not in {"developer", "creator"}:
        return
    staff = [(uid, u) for uid, u in users.items() if u.get("role", "student") != "student"]
    if not staff:
        await message.answer("🛡 Назначенного персонала пока нет.")
        return
    await message.answer(f"🛡 Персонал: {len(staff)}")
    for uid, u in staff[:30]:
        await message.answer(developer_user_card(uid, u), reply_markup=user_manage_keyboard(uid))

@dp.callback_query(F.data.startswith("user:"))
async def callback_user(callback: CallbackQuery):
    uid = callback.data.split(":", 1)[1]
    if get_role(callback.from_user.id) not in {"developer", "creator"}:
        await callback.answer("Нет доступа", show_alert=True)
        return
    if uid not in users:
        await callback.answer("Пользователь не найден", show_alert=True)
        return
    await callback.message.edit_text(developer_user_card(uid, users[uid]), reply_markup=user_manage_keyboard(uid))
    await callback.answer()

@dp.callback_query(F.data.startswith("roles:"))
async def callback_roles(callback: CallbackQuery):
    uid = callback.data.split(":", 1)[1]
    if not can_manage(callback.from_user.id, uid):
        await callback.answer("Недостаточно прав", show_alert=True)
        return
    await callback.message.edit_reply_markup(reply_markup=role_keyboard(uid))
    await callback.answer()

@dp.callback_query(F.data.startswith("setrole:"))
async def callback_set_role(callback: CallbackQuery):
    _, uid, new_role = callback.data.split(":", 2)
    if uid not in users or new_role not in ROLE_LABELS:
        await callback.answer("Ошибка данных", show_alert=True)
        return
    if not can_manage(callback.from_user.id, uid, new_role):
        await callback.answer("Недостаточно прав", show_alert=True)
        return
    # Developer cannot be assigned through buttons.
    if new_role == "developer":
        await callback.answer("Роль разработчика назначается только через PIN.", show_alert=True)
        return
    users[uid]["role"] = new_role
    save_users()
    await callback.message.edit_text(developer_user_card(uid, users[uid]), reply_markup=user_manage_keyboard(uid))
    await callback.answer(f"Назначено: {role_label(new_role)}")

@dp.callback_query(F.data.startswith("ban:"))
async def callback_ban(callback: CallbackQuery):
    uid = callback.data.split(":", 1)[1]
    if uid not in users:
        await callback.answer("Пользователь не найден", show_alert=True)
        return
    if not can_manage(callback.from_user.id, uid):
        await callback.answer("Недостаточно прав", show_alert=True)
        return
    if str(callback.from_user.id) == uid:
        await callback.answer("Нельзя заблокировать самого себя", show_alert=True)
        return
    if users[uid].get("role") == "developer":
        await callback.answer("Разработчика блокировать нельзя", show_alert=True)
        return
    users[uid]["banned"] = not users[uid].get("banned", False)
    save_users()
    await callback.message.edit_text(developer_user_card(uid, users[uid]), reply_markup=user_manage_keyboard(uid))
    await callback.answer("Статус блокировки изменён")

@dp.message(F.text == "🚪 Выйти из панели")
async def developer_logout(message: Message):
    if get_role(message.from_user.id) not in {"developer", "creator"}:
        return
    language = get_language(message.from_user.id)
    class_name = get_class(message.from_user.id)
    if language and class_name:
        await message.answer("🚪 Панель закрыта.", reply_markup=main_menu(message.from_user.id))
    elif language:
        await message.answer("🚪 Панель закрыта.", reply_markup=class_menu)
    else:
        await message.answer("🚪 Панель закрыта.", reply_markup=language_menu)


# ============================================================
# START
# ============================================================

@dp.message(CommandStart())
async def start(message: Message):

    user_id = message.from_user.id

    create_user(user_id, message.from_user)

    if is_banned(user_id):
        await message.answer("🚫 Доступ к боту для вашего аккаунта заблокирован.")
        return

    language = get_language(user_id)
    class_name = get_class(user_id)

    if not language:

        await message.answer(
            "🏫 Welcome / Добро пожаловать / Xush kelibsiz!\n\n"
            "🌐 Выбери язык / Choose your language / Tilni tanlang:",
            reply_markup=language_menu
        )
        return

    if not class_name:

        await message.answer(
            TEXTS[language]["choose_class"],
            reply_markup=class_menu
        )
        return

    await message.answer(
        f"🏫 {class_name}\n\n"
        f"{TEXTS[language]['choose_class']}",
        reply_markup=main_menu(user_id)
    )


# ============================================================
# ВЫБОР ЯЗЫКА
# ============================================================

@dp.message(F.text.in_(LANGUAGES.keys()))
async def select_language(message: Message):

    user_id = message.from_user.id

    create_user(user_id)

    language = LANGUAGES[message.text]

    users[str(user_id)]["language"] = language

    save_users()

    class_name = get_class(user_id)

    if not class_name:

        await message.answer(
            TEXTS[language]["choose_class"],
            reply_markup=class_menu
        )

    else:

        await message.answer(
            TEXTS[language]["welcome"].split("\n\n")[0],
            reply_markup=main_menu(user_id)
        )


# ============================================================
# ВЫБОР КЛАССА
# ============================================================

@dp.message(F.text.in_(CLASSES))
async def select_class(message: Message):

    user_id = message.from_user.id

    create_user(user_id)

    language = get_language(user_id)

    if not language:

        await message.answer(
            "🌐 Сначала выбери язык.",
            reply_markup=language_menu
        )
        return

    users[str(user_id)]["class"] = message.text

    save_users()

    await message.answer(
        TEXTS[language]["class_selected"].format(
            class_name=message.text
        ),
        reply_markup=main_menu(user_id)
    )


# ============================================================
# СМЕНА КЛАССА
# ============================================================

@dp.message(F.text.startswith("🎓"))
async def change_class(message: Message):

    user_id = message.from_user.id

    language = get_language(user_id)
    class_name = get_class(user_id)

    if not language:
        await message.answer(
            "🌐 Сначала выбери язык.",
            reply_markup=language_menu
        )
        return

    await message.answer(
        TEXTS[language]["change_class_text"].format(
            class_name=class_name
        ),
        reply_markup=class_menu
    )


# ============================================================
# СМЕНА ЯЗЫКА
# ============================================================

@dp.message(
    F.text.in_({
        "🌐 Язык: Русский",
        "🌐 Til: O‘zbekcha",
        "🌐 Language: English"
    })
)
async def change_language(message: Message):

    await message.answer(
        "🌐 Выбери язык / Choose language / Tilni tanlang:",
        reply_markup=language_menu
    )


# ============================================================
# РАСПИСАНИЕ
# ============================================================

async def send_schedule(message: Message):

    user_id = message.from_user.id

    language = get_language(user_id)
    class_name = get_class(user_id)

    if not language:
        await message.answer(
            "🌐 Сначала выбери язык.",
            reply_markup=language_menu
        )
        return

    if not class_name:
        await message.answer(
            TEXTS[language]["no_class"],
            reply_markup=class_menu
        )
        return

    if class_name not in SCHEDULES:

        await message.answer(
            TEXTS[language]["no_schedule"].format(
                class_name=class_name
            )
        )
        return

    schedule = SCHEDULES[class_name]

    text = TEXTS[language]["schedule_title"].format(
        class_name=class_name
    )

    for day, lessons in schedule.items():

        text += "\n\n━━━━━━━━━━━━━━\n"

        text += f"📌 {DAY_NAMES[language][day]}\n\n"

        for number, (time, subject) in enumerate(
            lessons,
            start=1
        ):

            translated_subject = SUBJECTS[language].get(
                subject,
                subject
            )

            text += (
                f"{number}. "
                f"{time} — "
                f"{translated_subject}\n"
            )

    await message.answer(text)


# ============================================================
# КНОПКА РАСПИСАНИЯ
# ============================================================

@dp.message(
    F.text.in_({
        "📅 Расписание",
        "📅 Dars jadvali",
        "📅 Schedule"
    })
)
async def schedule(message: Message):

    await send_schedule(message)


# ============================================================
# УЧЕБНИКИ
# ============================================================

@dp.message(
    F.text.in_({
        "📚 Учебники",
        "📚 Darsliklar",
        "📚 Textbooks"
    })
)
async def books(message: Message):

    user_id = message.from_user.id

    language = get_language(user_id)
    class_name = get_class(user_id)

    if not language:
        await message.answer(
            "🌐 Сначала выбери язык.",
            reply_markup=language_menu
        )
        return

    if not class_name:
        await message.answer(
            TEXTS[language]["no_class"],
            reply_markup=class_menu
        )
        return

    await message.answer(
        TEXTS[language]["books_text"].format(
            class_name=class_name
        )
    )


# ============================================================
# ДОМАШНИЕ ЗАДАНИЯ
# ============================================================

@dp.message(
    F.text.in_({
        "📝 Домашние задания",
        "📝 Uy vazifalari",
        "📝 Homework"
    })
)
async def homework(message: Message):

    user_id = message.from_user.id

    language = get_language(user_id)
    class_name = get_class(user_id)

    if not language:
        await message.answer(
            "🌐 Сначала выбери язык.",
            reply_markup=language_menu
        )
        return

    if not class_name:
        await message.answer(
            TEXTS[language]["no_class"],
            reply_markup=class_menu
        )
        return

    await message.answer(
        TEXTS[language]["homework_text"].format(
            class_name=class_name
        )
    )


# ============================================================
# НОВОСТИ
# ============================================================

@dp.message(
    F.text.in_({
        "📢 Новости",
        "📢 Yangiliklar",
        "📢 News"
    })
)
async def news(message: Message):

    user_id = message.from_user.id

    language = get_language(user_id)
    class_name = get_class(user_id)

    if not language:
        await message.answer(
            "🌐 Сначала выбери язык.",
            reply_markup=language_menu
        )
        return

    if not class_name:
        await message.answer(
            TEXTS[language]["no_class"],
            reply_markup=class_menu
        )
        return

    await message.answer(
        TEXTS[language]["news_text"]
    )


# ============================================================
# КОНТАКТЫ
# ============================================================

@dp.message(
    F.text.in_({
        "☎️ Контакты",
        "☎️ Aloqa",
        "☎️ Contacts"
    })
)
async def contacts(message: Message):

    user_id = message.from_user.id

    language = get_language(user_id)
    class_name = get_class(user_id)

    if not language:
        await message.answer(
            "🌐 Сначала выбери язык.",
            reply_markup=language_menu
        )
        return

    if not class_name:
        await message.answer(
            TEXTS[language]["no_class"],
            reply_markup=class_menu
        )
        return

    await message.answer(
        TEXTS[language]["contacts_text"]
    )


# ============================================================
# ПОМОЩЬ
# ============================================================

@dp.message(
    F.text.in_({
        "ℹ️ Помощь",
        "ℹ️ Yordam",
        "ℹ️ Help"
    })
)
async def help_command(message: Message):

    user_id = message.from_user.id

    language = get_language(user_id)
    class_name = get_class(user_id)

    if not language:
        await message.answer(
            "🌐 Сначала выбери язык.",
            reply_markup=language_menu
        )
        return

    if not class_name:
        await message.answer(
            TEXTS[language]["no_class"],
            reply_markup=class_menu
        )
        return

    await message.answer(
        TEXTS[language]["help_text"].format(
            class_name=class_name
        )
    )


# ============================================================
# ЗАПУСК
# ============================================================

async def main():

    bot = Bot(token=BOT_TOKEN)

    print("🤖 Бот запущен!")
    print("🌐 Языки: RU / UZ / EN")
    print("🎓 Классы: 1А–11А/Б")
    print("📅 Расписание: 6Б / 7А / 8А")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
