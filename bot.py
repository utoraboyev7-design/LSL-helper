import asyncio
import json
import os
import hashlib
import hmac
import time
from urllib.parse import parse_qsl
from pathlib import Path
from aiohttp import web

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,
                           InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, WebAppInfo,
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

DATA_DIR = os.getenv("DATA_DIR", ".")
os.makedirs(DATA_DIR, exist_ok=True)
DATA_FILE = os.path.join(DATA_DIR, "users.json")
GROUPS_FILE = os.path.join(DATA_DIR, "groups.json")

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
    "8Б",
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

    "8Б": {
        "Понедельник": [
            ("8:30–9:15", "Algebra"),
            ("9:25–10:10", "Fizika"),
            ("10:20–11:05", "Rus tili"),
            ("11:15–12:00", "Biologiya"),
            ("13:00–13:45", "Chet tili"),
            ("13:55–14:40", "Chet tili"),
            ("14:50–15:35", "Algebra"),
            ("15:45–16:30", "Geografiya"),
        ],
        "Вторник": [
            ("8:30–9:15", "Informatika"),
            ("9:25–10:10", "Informatika"),
            ("10:20–11:05", "Texnologiya"),
            ("11:15–12:00", "Tarix"),
            ("13:00–13:45", "Chet tili"),
            ("13:55–14:40", "Chet tili"),
            ("14:50–15:35", "Matematika"),
            ("15:45–16:30", "Informatika"),
        ],
        "Среда": [
            ("8:30–9:15", "Tarbiya"),
            ("9:25–10:10", "Rus tili"),
            ("10:20–11:05", "Geografiya"),
            ("11:15–12:00", "Chet tili"),
            ("13:00–13:45", "Chet tili"),
            ("13:55–14:40", "Chet tili"),
            ("14:50–15:35", "Algebra"),
            ("15:45–16:30", "Geometriya"),
        ],
        "Четверг": [
            ("8:30–9:15", "Adabiyot"),
            ("9:25–10:10", "Kimyo"),
            ("10:20–11:05", "Huquq"),
            ("11:15–12:00", "Biologiya"),
            ("13:00–13:45", "Chet tili"),
            ("13:55–14:40", "Chet tili"),
            ("14:50–15:35", "Tasv/Chizma"),
            ("15:45–16:30", "Ona tili"),
        ],
        "Пятница": [
            ("8:30–9:15", "Tarix"),
            ("9:25–10:10", "Biologiya"),
            ("10:20–11:05", "Kimyo"),
            ("11:15–12:00", "Algebra"),
            ("13:00–13:45", "Sinf soati"),
            ("13:55–14:40", "Geometriya"),
            ("14:50–15:35", "Mat. kurs"),
            ("15:45–16:30", "Mat. kurs"),
        ],
        "Суббота": [
            ("8:30–9:15", "Chet tili"),
            ("9:25–10:10", "Fizika"),
            ("10:20–11:05", "Jis/tar"),
            ("11:15–12:00", "Jis/tar"),
            ("13:00–13:45", "Informatika"),
            ("13:55–14:40", "Informatika"),
            ("14:50–15:35", "Chet tili"),
            ("15:45–16:30", "Chet tili"),
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
    user.setdefault("warnings", {})
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
        [KeyboardButton(text="8А"), KeyboardButton(text="8Б")],
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
        [InlineKeyboardButton(text="🔇 Мут", callback_data=f"pmute:{user_id}"),
         InlineKeyboardButton(text="🔊 Размут", callback_data=f"punmute:{user_id}")],
        [InlineKeyboardButton(text="👢 Кик", callback_data=f"pkick:{user_id}"),
         InlineKeyboardButton(text="⛔ Бан в группе", callback_data=f"pgroupban:{user_id}")],
        [InlineKeyboardButton(text="🎖 Изменить должность", callback_data=f"roles:{user_id}")],
        [InlineKeyboardButton(
            text="✅ Разбанить в боте" if users.get(str(user_id), {}).get("banned") else "🚫 Заблокировать в боте",
            callback_data=f"ban:{user_id}"
        )]
    ])

def moderation_group_keyboard(action, user_id):
    rows = []
    active = [(gid, g) for gid, g in groups.items() if g.get("active", True)]
    for gid, g in active[:25]:
        title = g.get("title", "Группа")
        rows.append([InlineKeyboardButton(
            text=f"🏫 {title[:32]}",
            callback_data=f"modgrp:{action}:{user_id}:{gid}"
        )])
    rows.append([InlineKeyboardButton(text="⬅️ Назад", callback_data=f"user:{user_id}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def mute_duration_keyboard(user_id, group_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="10 мин", callback_data=f"domute:{user_id}:{group_id}:10"),
         InlineKeyboardButton(text="30 мин", callback_data=f"domute:{user_id}:{group_id}:30")],
        [InlineKeyboardButton(text="1 час", callback_data=f"domute:{user_id}:{group_id}:60"),
         InlineKeyboardButton(text="6 часов", callback_data=f"domute:{user_id}:{group_id}:360")],
        [InlineKeyboardButton(text="1 день", callback_data=f"domute:{user_id}:{group_id}:1440"),
         InlineKeyboardButton(text="7 дней", callback_data=f"domute:{user_id}:{group_id}:10080")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data=f"pmute:{user_id}")]
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


def _target_from_reply(message: Message):
    if not message.reply_to_message or not message.reply_to_message.from_user:
        return None
    return message.reply_to_message.from_user

def _group_staff_allowed(actor_id, target_id):
    return can_group_moderate(actor_id, target_id)

@dp.message(Command("warn"))
async def group_warn(message: Message):
    if message.chat.type not in {"group", "supergroup"}:
        return
    remember_group(message.chat)
    create_user(message.from_user.id, message.from_user)
    target = _target_from_reply(message)
    if not target:
        if get_role(message.from_user.id) in GROUP_MOD_ROLES:
            await message.reply("⚠️ Ответь /warn на сообщение пользователя.")
        return
    create_user(target.id, target)
    if not _group_staff_allowed(message.from_user.id, target.id):
        await message.reply("⛔ Недостаточно прав.")
        return
    gid = str(message.chat.id)
    warnings = users[str(target.id)].setdefault("warnings", {})
    warnings[gid] = int(warnings.get(gid, 0)) + 1
    save_users()
    reason = (message.text or "").partition(" ")[2].strip() or "Причина не указана"
    await message.reply(
        f"⚠️ Варн: {target.full_name}\n"
        f"📌 Причина: {reason}\n"
        f"🔢 Варнов: {warnings[gid]}/3"
    )
    if warnings[gid] >= 3:
        try:
            await message.bot.ban_chat_member(message.chat.id, target.id)
            warnings[gid] = 0
            save_users()
            await message.reply("⛔ 3/3 варнов — пользователь забанен в этой группе.")
        except Exception:
            await message.reply("❌ 3/3 варнов, но бан не прошёл. Проверь право бота блокировать участников.")

@dp.message(Command("warns"))
async def group_warns(message: Message):
    if message.chat.type not in {"group", "supergroup"}:
        return
    create_user(message.from_user.id, message.from_user)
    if get_role(message.from_user.id) not in GROUP_MOD_ROLES:
        return
    target = _target_from_reply(message)
    if not target:
        await message.reply("⚠️ Ответь /warns на сообщение пользователя.")
        return
    create_user(target.id, target)
    count = users[str(target.id)].setdefault("warnings", {}).get(str(message.chat.id), 0)
    await message.reply(f"⚠️ {target.full_name}: {count}/3 варнов.")

@dp.message(Command("clearwarns"))
async def group_clearwarns(message: Message):
    if message.chat.type not in {"group", "supergroup"}:
        return
    create_user(message.from_user.id, message.from_user)
    target = _target_from_reply(message)
    if not target:
        if get_role(message.from_user.id) in GROUP_MOD_ROLES:
            await message.reply("⚠️ Ответь /clearwarns на сообщение пользователя.")
        return
    create_user(target.id, target)
    if not _group_staff_allowed(message.from_user.id, target.id):
        await message.reply("⛔ Недостаточно прав.")
        return
    users[str(target.id)].setdefault("warnings", {})[str(message.chat.id)] = 0
    save_users()
    await message.reply(f"✅ Варны {target.full_name} очищены.")

@dp.message(Command("ban"))
async def group_ban_command(message: Message):
    if message.chat.type not in {"group", "supergroup"}:
        return
    remember_group(message.chat)
    create_user(message.from_user.id, message.from_user)
    target = _target_from_reply(message)
    if not target:
        if get_role(message.from_user.id) in GROUP_MOD_ROLES:
            await message.reply("⚠️ Ответь /ban на сообщение пользователя.")
        return
    create_user(target.id, target)
    if not _group_staff_allowed(message.from_user.id, target.id):
        await message.reply("⛔ Недостаточно прав.")
        return
    try:
        await message.bot.ban_chat_member(message.chat.id, target.id)
        await message.reply(f"⛔ {target.full_name} забанен.")
    except Exception:
        await message.reply("❌ Не получилось. Проверь право бота блокировать участников.")

@dp.message(Command("unban"))
async def group_unban_command(message: Message):
    if message.chat.type not in {"group", "supergroup"}:
        return
    create_user(message.from_user.id, message.from_user)
    if get_role(message.from_user.id) not in GROUP_MOD_ROLES:
        return
    parts = (message.text or "").split()
    if len(parts) != 2 or not parts[1].lstrip("-").isdigit():
        await message.reply("Формат: /unban TELEGRAM_ID")
        return
    target_id = int(parts[1])
    create_user(target_id)
    if not _group_staff_allowed(message.from_user.id, target_id):
        await message.reply("⛔ Недостаточно прав.")
        return
    try:
        await message.bot.unban_chat_member(message.chat.id, target_id, only_if_banned=True)
        await message.reply("✅ Пользователь разбанен.")
    except Exception:
        await message.reply("❌ Не получилось разбанить.")

@dp.message(Command("kick"))
async def group_kick_command(message: Message):
    if message.chat.type not in {"group", "supergroup"}:
        return
    remember_group(message.chat)
    create_user(message.from_user.id, message.from_user)
    target = _target_from_reply(message)
    if not target:
        if get_role(message.from_user.id) in GROUP_MOD_ROLES:
            await message.reply("⚠️ Ответь /kick на сообщение пользователя.")
        return
    create_user(target.id, target)
    if not _group_staff_allowed(message.from_user.id, target.id):
        await message.reply("⛔ Недостаточно прав.")
        return
    try:
        await message.bot.ban_chat_member(message.chat.id, target.id)
        await message.bot.unban_chat_member(message.chat.id, target.id, only_if_banned=True)
        await message.reply(f"👢 {target.full_name} кикнут.")
    except Exception:
        await message.reply("❌ Не получилось. Проверь права бота.")


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
    if message.chat.type != "private":
        return

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
    if message.chat.type != "private":
        return

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
    if message.chat.type != "private":
        return

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
    if message.chat.type != "private":
        return

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
    if message.chat.type != "private":
        return

    if get_role(message.from_user.id) not in {"developer", "creator"}:
        return
    await state.set_state(DeveloperAction.waiting_for_user)
    await message.answer("🔎 Отправь Telegram ID или @username пользователя:", reply_markup=ReplyKeyboardRemove())

@dp.message(DeveloperAction.waiting_for_user)
async def find_user_finish(message: Message, state: FSMContext):
    if message.chat.type != "private":
        return

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
    if message.chat.type != "private":
        return

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
    if message.chat.type != "private":
        return

    if get_role(message.from_user.id) not in {"developer", "creator"}:
        return
    staff = [(uid, u) for uid, u in users.items() if u.get("role", "student") != "student"]
    if not staff:
        await message.answer("🛡 Назначенного персонала пока нет.")
        return
    await message.answer(f"🛡 Персонал: {len(staff)}")
    for uid, u in staff[:30]:
        await message.answer(developer_user_card(uid, u), reply_markup=user_manage_keyboard(uid))


def _panel_mod_allowed(actor_id, target_id):
    return can_group_moderate(actor_id, target_id)

@dp.callback_query(F.data.startswith("pmute:"))
async def panel_mute_choose_group(callback: CallbackQuery):
    if not callback.message or callback.message.chat.type != "private":
        await callback.answer()
        return
    uid = callback.data.split(":", 1)[1]
    if uid not in users or not _panel_mod_allowed(callback.from_user.id, uid):
        await callback.answer("Недостаточно прав", show_alert=True)
        return
    active = [g for g in groups.values() if g.get("active", True)]
    if not active:
        await callback.answer("Нет сохранённых групп", show_alert=True)
        return
    await callback.message.edit_text(
        "🔇 Выбери группу для мута:",
        reply_markup=moderation_group_keyboard("mute", uid)
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("punmute:"))
async def panel_unmute_choose_group(callback: CallbackQuery):
    if not callback.message or callback.message.chat.type != "private":
        await callback.answer()
        return
    uid = callback.data.split(":", 1)[1]
    if uid not in users or not _panel_mod_allowed(callback.from_user.id, uid):
        await callback.answer("Недостаточно прав", show_alert=True)
        return
    await callback.message.edit_text(
        "🔊 Выбери группу:",
        reply_markup=moderation_group_keyboard("unmute", uid)
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("pkick:"))
async def panel_kick_choose_group(callback: CallbackQuery):
    if not callback.message or callback.message.chat.type != "private":
        await callback.answer()
        return
    uid = callback.data.split(":", 1)[1]
    if uid not in users or not _panel_mod_allowed(callback.from_user.id, uid):
        await callback.answer("Недостаточно прав", show_alert=True)
        return
    await callback.message.edit_text(
        "👢 Выбери группу для кика:",
        reply_markup=moderation_group_keyboard("kick", uid)
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("pgroupban:"))
async def panel_ban_choose_group(callback: CallbackQuery):
    if not callback.message or callback.message.chat.type != "private":
        await callback.answer()
        return
    uid = callback.data.split(":", 1)[1]
    if uid not in users or not _panel_mod_allowed(callback.from_user.id, uid):
        await callback.answer("Недостаточно прав", show_alert=True)
        return
    await callback.message.edit_text(
        "⛔ Выбери группу для бана:",
        reply_markup=moderation_group_keyboard("ban", uid)
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("modgrp:"))
async def panel_group_action(callback: CallbackQuery, bot: Bot):
    if not callback.message or callback.message.chat.type != "private":
        await callback.answer()
        return

    _, action, uid, group_id = callback.data.split(":", 3)
    if uid not in users or not _panel_mod_allowed(callback.from_user.id, uid):
        await callback.answer("Недостаточно прав", show_alert=True)
        return
    if group_id not in groups or not groups[group_id].get("active", True):
        await callback.answer("Группа недоступна", show_alert=True)
        return

    if action == "mute":
        await callback.message.edit_text(
            f"🔇 Выбери срок мута\\n🏫 {groups[group_id].get('title', 'Группа')}",
            reply_markup=mute_duration_keyboard(uid, group_id)
        )
        await callback.answer()
        return

    try:
        gid = int(group_id)
        target_id = int(uid)

        if action == "unmute":
            await bot.restrict_chat_member(
                chat_id=gid,
                user_id=target_id,
                permissions=ChatPermissions(
                    can_send_messages=True, can_send_audios=True,
                    can_send_documents=True, can_send_photos=True,
                    can_send_videos=True, can_send_video_notes=True,
                    can_send_voice_notes=True, can_send_polls=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True,
                    can_change_info=False, can_invite_users=True,
                    can_pin_messages=False, can_manage_topics=False
                )
            )
            result = "🔊 Мут снят."
        elif action == "kick":
            await bot.ban_chat_member(chat_id=gid, user_id=target_id)
            await bot.unban_chat_member(chat_id=gid, user_id=target_id, only_if_banned=True)
            result = "👢 Пользователь кикнут."
        elif action == "ban":
            await bot.ban_chat_member(chat_id=gid, user_id=target_id)
            result = "⛔ Пользователь забанен в группе."
        else:
            await callback.answer("Неизвестное действие", show_alert=True)
            return

        await callback.message.edit_text(
            result + f"\\n🏫 {groups[group_id].get('title', 'Группа')}",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ К пользователю", callback_data=f"user:{uid}")]
            ])
        )
        await callback.answer("Готово")
    except Exception:
        await callback.answer(
            "Не получилось. Проверь админ-права бота в этой группе.",
            show_alert=True
        )

@dp.callback_query(F.data.startswith("domute:"))
async def panel_do_mute(callback: CallbackQuery, bot: Bot):
    if not callback.message or callback.message.chat.type != "private":
        await callback.answer()
        return

    _, uid, group_id, minutes_raw = callback.data.split(":", 3)
    if uid not in users or not _panel_mod_allowed(callback.from_user.id, uid):
        await callback.answer("Недостаточно прав", show_alert=True)
        return

    try:
        minutes = int(minutes_raw)
        from datetime import datetime, timedelta, timezone
        until = datetime.now(timezone.utc) + timedelta(minutes=minutes)

        await bot.restrict_chat_member(
            chat_id=int(group_id),
            user_id=int(uid),
            permissions=ChatPermissions(
                can_send_messages=False, can_send_audios=False,
                can_send_documents=False, can_send_photos=False,
                can_send_videos=False, can_send_video_notes=False,
                can_send_voice_notes=False, can_send_polls=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False,
                can_change_info=False, can_invite_users=False,
                can_pin_messages=False, can_manage_topics=False
            ),
            until_date=until
        )

        await callback.message.edit_text(
            f"🔇 Мут выдан на {minutes} мин.\\n"
            f"🏫 {groups.get(group_id, {}).get('title', 'Группа')}",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ К пользователю", callback_data=f"user:{uid}")]
            ])
        )
        await callback.answer("Готово")
    except Exception:
        await callback.answer(
            "Не получилось выдать мут. Проверь права бота и наличие пользователя в группе.",
            show_alert=True
        )


@dp.callback_query(F.data.startswith("user:"))
async def callback_user(callback: CallbackQuery):
    if not callback.message or callback.message.chat.type != "private":
        await callback.answer()
        return

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
    if not callback.message or callback.message.chat.type != "private":
        await callback.answer()
        return

    uid = callback.data.split(":", 1)[1]
    if not can_manage(callback.from_user.id, uid):
        await callback.answer("Недостаточно прав", show_alert=True)
        return
    await callback.message.edit_reply_markup(reply_markup=role_keyboard(uid))
    await callback.answer()

@dp.callback_query(F.data.startswith("setrole:"))
async def callback_set_role(callback: CallbackQuery):
    if not callback.message or callback.message.chat.type != "private":
        await callback.answer()
        return

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
    if not callback.message or callback.message.chat.type != "private":
        await callback.answer()
        return

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
    if message.chat.type != "private":
        return

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
    if message.chat.type != "private":
        return


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
    if message.chat.type != "private":
        return


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
    if message.chat.type != "private":
        return


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
    if message.chat.type != "private":
        return


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
    if message.chat.type != "private":
        return


    await message.answer(
        "🌐 Выбери язык / Choose language / Tilni tanlang:",
        reply_markup=language_menu
    )


# ============================================================
# РАСПИСАНИЕ
# ============================================================

async def send_schedule(message: Message):
    if message.chat.type != "private":
        return


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
    if message.chat.type != "private":
        return


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
    if message.chat.type != "private":
        return


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
    if message.chat.type != "private":
        return

    user_id = message.from_user.id
    create_user(user_id, message.from_user)
    language = get_language(user_id)
    class_name = get_class(user_id)

    if not language:
        await message.answer("🌐 Сначала выбери язык.", reply_markup=language_menu)
        return
    if not class_name:
        await message.answer(TEXTS[language]["no_class"], reply_markup=class_menu)
        return

    text = content_data.get("homework", {}).get(class_name, "").strip()
    if text:
        titles = {"ru": "📝 Домашнее задание", "uz": "📝 Uy vazifasi", "en": "📝 Homework"}
        await message.answer(f"{titles.get(language, titles['ru'])} — {class_name}\n\n{text}")
    else:
        empty = {
            "ru": f"📝 Для класса {class_name} домашнее задание пока не добавлено.",
            "uz": f"📝 {class_name} sinfi uchun uy vazifasi hali qo‘shilmagan.",
            "en": f"📝 No homework has been added for {class_name} yet."
        }
        await message.answer(empty.get(language, empty["ru"]))


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
    if message.chat.type != "private":
        return

    user_id = message.from_user.id
    create_user(user_id, message.from_user)
    language = get_language(user_id)
    class_name = get_class(user_id)

    if not language:
        await message.answer("🌐 Сначала выбери язык.", reply_markup=language_menu)
        return
    if not class_name:
        await message.answer(TEXTS[language]["no_class"], reply_markup=class_menu)
        return

    text = str(content_data.get("news", "")).strip()
    if text:
        titles = {"ru": "📢 Новости LSL", "uz": "📢 LSL yangiliklari", "en": "📢 LSL News"}
        await message.answer(f"{titles.get(language, titles['ru'])}\n\n{text}")
    else:
        empty = {
            "ru": "📢 Новостей пока нет.",
            "uz": "📢 Hozircha yangiliklar yo‘q.",
            "en": "📢 There are no news posts yet."
        }
        await message.answer(empty.get(language, empty["ru"]))


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
    if message.chat.type != "private":
        return


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
    if message.chat.type != "private":
        return


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




async def send_saved_homework(message: Message):
    if message.chat.type != "private":
        return
    uid = str(message.from_user.id)
    class_name = get_class(uid)
    language = get_language(uid) or "ru"
    text = content_data.get("homework", {}).get(class_name, "").strip()
    if text:
        await message.answer(f"📚 {class_name}\n\n{text}")
    else:
        await message.answer("📚 Домашнее задание для вашего класса пока не добавлено.")

# ============================================================
# MINI APP
# ============================================================

WEBAPP_URL = os.getenv("WEBAPP_URL", "").rstrip("/")
CONTENT_FILE = os.path.join(DATA_DIR, "content.json")

def load_content():
    default = {"news": "", "homework": {}, "audit": []}
    if not os.path.exists(CONTENT_FILE):
        return default
    try:
        with open(CONTENT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        data.setdefault("news", "")
        data.setdefault("homework", {})
        data.setdefault("audit", [])
        return data
    except Exception:
        return default

content_data = load_content()

def save_content():
    with open(CONTENT_FILE, "w", encoding="utf-8") as f:
        json.dump(content_data, f, ensure_ascii=False, indent=2)

def validate_init_data(init_data: str):
    if not init_data or not BOT_TOKEN:
        return None
    try:
        pairs = dict(parse_qsl(init_data, keep_blank_values=True))
        received_hash = pairs.pop("hash", None)
        if not received_hash:
            return None
        data_check = "\n".join(f"{k}={v}" for k, v in sorted(pairs.items()))
        secret = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
        expected = hmac.new(secret, data_check.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, received_hash):
            return None
        auth_date = int(pairs.get("auth_date", "0"))
        if abs(int(time.time()) - auth_date) > 86400:
            return None
        return json.loads(pairs.get("user", "{}"))
    except Exception:
        return None


def make_mini_session(user_id):
    ts = int(time.time())
    payload = f"{user_id}:{ts}"
    sig = hmac.new(BOT_TOKEN.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}:{sig}"

def validate_mini_session(token):
    try:
        uid, ts, sig = token.split(":", 2)
        if abs(int(time.time()) - int(ts)) > 3600:
            return None
        payload = f"{uid}:{ts}"
        expected = hmac.new(BOT_TOKEN.encode(), payload.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected):
            return None
        return uid
    except Exception:
        return None

def panel_permissions(role):
    level = ROLE_LEVELS.get(role, 0)
    return {
        "homework": role in {"teacher","junior_admin","admin","zga","ga","creator","developer"},
        "news": level >= ROLE_LEVELS["admin"],
        "users": level >= ROLE_LEVELS["junior_moder"],
        "group_moderation": role in GROUP_MOD_ROLES,
        "bot_ban": level >= ROLE_LEVELS["junior_admin"],
        "roles": level >= ROLE_LEVELS["admin"],
        "staff": level >= ROLE_LEVELS["zga"],
        "full": role in {"creator","developer"},
    }

def mini_actor(request):
    uid = None
    tg_user = validate_init_data(request.headers.get("X-Telegram-Init-Data", ""))
    if tg_user and "id" in tg_user:
        uid = str(tg_user["id"])
    if not uid:
        uid = validate_mini_session(request.headers.get("X-LSL-Session", ""))
    if not uid or uid not in users:
        return None
    role = get_role(uid)
    # Student has no staff panel. Teacher and every staff rank have their own panel.
    if role == "student":
        return None
    return uid

async def mini_index(request):
    return web.FileResponse(Path(__file__).with_name("miniapp.html"))


def json_safe(value):
    if isinstance(value, set):
        return sorted(list(value))
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    return value

def public_user(user_id, u):
    return {
        "id": str(user_id),
        "name": " ".join(x for x in [u.get("first_name"), u.get("last_name")] if x) or "Без имени",
        "username": u.get("username"),
        "class": u.get("class"),
        "language": u.get("language"),
        "role": u.get("role", "student"),
        "role_label": role_label(u.get("role", "student")),
        "banned": bool(u.get("banned", False)),
    }

def mini_can_manage(actor_id, target_id, new_role=None):
    actor_role = get_role(actor_id)
    target_role = get_role(target_id)
    if not panel_permissions(actor_role)["roles"]:
        return False
    if actor_role == "developer":
        return new_role != "developer" or str(actor_id) == str(target_id)
    if target_role == "developer" or new_role == "developer":
        return False
    if actor_role == "creator":
        return target_role != "developer" and new_role != "developer"
    actor_level = ROLE_LEVELS.get(actor_role, 0)
    target_level = ROLE_LEVELS.get(target_role, 0)
    new_level = ROLE_LEVELS.get(new_role, 0) if new_role else 0
    return target_level < actor_level and (not new_role or new_level < actor_level)

def add_audit(actor_id, action, target=None, extra=None):
    item = {
        "ts": int(time.time()),
        "actor": str(actor_id),
        "action": action,
        "target": str(target) if target is not None else None,
        "extra": extra or {}
    }
    content_data.setdefault("audit", []).append(item)
    content_data["audit"] = content_data["audit"][-300:]
    save_content()

async def mini_me(request):
    uid = mini_actor(request)
    if not uid:
        return web.json_response({"error": "forbidden"}, status=403)
    role = get_role(uid)
    return web.json_response(json_safe({
        "id": uid,
        "role": role,
        "role_label": role_label(role),
        "role_level": ROLE_LEVELS.get(role, 0),
        "permissions": panel_permissions(role),
        "users": len(users),
        "classes": sorted(list(CLASSES)),
        "groups": [{"id": gid, **g} for gid, g in groups.items() if g.get("active", True)],
        "news": content_data.get("news", ""),
        "homework": content_data.get("homework", {}),
        "audit": content_data.get("audit", [])[-30:]
    }))

async def mini_users(request):
    uid = mini_actor(request)
    if not uid or not panel_permissions(get_role(uid))["users"]:
        return web.json_response({"error": "forbidden"}, status=403)
    return web.json_response([public_user(user_id, u) for user_id, u in list(users.items())[-500:]])

async def mini_save_news(request):
    uid = mini_actor(request)
    if not uid or ROLE_LEVELS.get(get_role(uid), 0) < ROLE_LEVELS["admin"]:
        return web.json_response({"error": "forbidden"}, status=403)
    body = await request.json()
    content_data["news"] = str(body.get("text", ""))[:10000]
    add_audit(uid, "news")
    save_content()
    return web.json_response({"ok": True})

async def mini_save_homework(request):
    uid = mini_actor(request)
    if not uid or not panel_permissions(get_role(uid))["homework"]:
        return web.json_response({"error": "forbidden"}, status=403)
    body = await request.json()
    class_name = str(body.get("class_name", "")).strip()
    text = str(body.get("text", ""))[:10000]
    if class_name not in CLASSES:
        return web.json_response({"error": "invalid class"}, status=400)
    content_data.setdefault("homework", {})[class_name] = text
    add_audit(uid, "homework", extra={"class": class_name})
    save_content()
    return web.json_response({"ok": True})

async def mini_user_role(request):
    actor = mini_actor(request)
    if not actor:
        return web.json_response({"error": "forbidden"}, status=403)
    target = request.match_info["uid"]
    body = await request.json()
    new_role = str(body.get("role", ""))
    if target not in users or new_role not in ROLE_LABELS or new_role == "developer":
        return web.json_response({"error": "bad request"}, status=400)
    if not mini_can_manage(actor, target, new_role):
        return web.json_response({"error": "forbidden"}, status=403)
    users[target]["role"] = new_role
    save_users()
    add_audit(actor, "role", target, {"role": new_role})
    return web.json_response({"ok": True, "user": public_user(target, users[target])})

async def mini_user_botban(request):
    actor = mini_actor(request)
    if not actor:
        return web.json_response({"error": "forbidden"}, status=403)
    target = request.match_info["uid"]
    if target not in users:
        return web.json_response({"error": "not found"}, status=404)
    actor_role, target_role = get_role(actor), get_role(target)
    if (not panel_permissions(actor_role)["bot_ban"] or
        ROLE_LEVELS.get(actor_role, 0) <= ROLE_LEVELS.get(target_role, 0)):
        return web.json_response({"error": "forbidden"}, status=403)
    body = await request.json()
    banned = bool(body.get("banned", True))
    users[target]["banned"] = banned
    save_users()
    add_audit(actor, "botban", target, {"banned": banned})
    return web.json_response({"ok": True, "user": public_user(target, users[target])})

async def mini_group_action(request):
    actor = mini_actor(request)
    if not actor:
        return web.json_response({"error": "forbidden"}, status=403)
    target = request.match_info["uid"]
    if target not in users or not can_group_moderate(actor, target):
        return web.json_response({"error": "forbidden"}, status=403)
    body = await request.json()
    action = str(body.get("action", ""))
    group_id = str(body.get("group_id", ""))
    minutes = int(body.get("minutes", 10) or 10)
    if group_id not in groups or not groups[group_id].get("active", True):
        return web.json_response({"error": "invalid group"}, status=400)
    gid, tid = int(group_id), int(target)
    try:
        if action == "mute":
            from datetime import datetime, timedelta, timezone
            until = datetime.now(timezone.utc) + timedelta(minutes=max(1, min(minutes, 10080)))
            await request.app["bot"].restrict_chat_member(
                gid, tid,
                permissions=ChatPermissions(
                    can_send_messages=False, can_send_audios=False, can_send_documents=False,
                    can_send_photos=False, can_send_videos=False, can_send_video_notes=False,
                    can_send_voice_notes=False, can_send_polls=False, can_send_other_messages=False,
                    can_add_web_page_previews=False, can_change_info=False, can_invite_users=False,
                    can_pin_messages=False, can_manage_topics=False
                ),
                until_date=until
            )
        elif action == "unmute":
            await request.app["bot"].restrict_chat_member(
                gid, tid,
                permissions=ChatPermissions(
                    can_send_messages=True, can_send_audios=True, can_send_documents=True,
                    can_send_photos=True, can_send_videos=True, can_send_video_notes=True,
                    can_send_voice_notes=True, can_send_polls=True, can_send_other_messages=True,
                    can_add_web_page_previews=True, can_change_info=False, can_invite_users=True,
                    can_pin_messages=False, can_manage_topics=False
                )
            )
        elif action == "kick":
            await request.app["bot"].ban_chat_member(gid, tid)
            await request.app["bot"].unban_chat_member(gid, tid, only_if_banned=True)
        elif action == "ban":
            await request.app["bot"].ban_chat_member(gid, tid)
        elif action == "warn":
            warnings = users[target].setdefault("warnings", {})
            warnings[group_id] = int(warnings.get(group_id, 0)) + 1
            save_users()
        elif action == "clearwarns":
            users[target].setdefault("warnings", {})[group_id] = 0
            save_users()
        else:
            return web.json_response({"error": "invalid action"}, status=400)
    except Exception as e:
        return web.json_response({"error": "telegram action failed", "detail": str(e)[:300]}, status=400)
    add_audit(actor, action, target, {"group_id": group_id, "minutes": minutes})
    return web.json_response({"ok": True})


@dp.message(Command("app"))
async def open_mini_app(message: Message):
    if message.chat.type != "private":
        return
    create_user(message.from_user.id, message.from_user)
    role = get_role(message.from_user.id)
    if role == "student":
        await message.answer("⛔ Для вашей роли административная панель не предусмотрена.")
        return
    if not WEBAPP_URL:
        await message.answer("⚠️ WEBAPP_URL ещё не настроен в Railway.")
        return
    session = make_mini_session(message.from_user.id)
    sep = "&" if "?" in WEBAPP_URL else "?"
    launch_url = f"{WEBAPP_URL}{sep}s={session}"
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=f"⚙️ Открыть панель • {role_label(role)}", web_app=WebAppInfo(url=launch_url))
    ]])
    await message.answer(f"⚙️ LSL Control\\n🛡 Ваша роль: {role_label(role)}", reply_markup=kb)

async def start_web_server(bot):
    app = web.Application()
    app["bot"] = bot
    app.router.add_get("/", mini_index)
    app.router.add_get("/api/me", mini_me)
    app.router.add_get("/api/users", mini_users)
    app.router.add_post("/api/news", mini_save_news)
    app.router.add_post("/api/homework", mini_save_homework)
    app.router.add_post("/api/users/{uid}/role", mini_user_role)
    app.router.add_post("/api/users/{uid}/botban", mini_user_botban)
    app.router.add_post("/api/users/{uid}/group-action", mini_group_action)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", "8080"))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"🌐 Mini App server: port {port}")
    return runner



# ============================================================
# АВАРИЙНОЕ ВОССТАНОВЛЕНИЕ РОЛИ ПО PIN
# ============================================================

@dp.message(Command("back"))
async def restore_role_by_pin(message: Message):
    parts = (message.text or "").split(maxsplit=2)

    if len(parts) != 3:
        await message.answer("Использование: /back ROLE PIN")
        return

    _, role_input, pin = parts

    if not DEVELOPER_PIN or pin != DEVELOPER_PIN:
        await message.answer("❌ Неверный PIN.")
        return

    role_map = {
        "developer": "developer",
        "creator": "creator",
        "ga": "ga",
        "zga": "zga",
        "admin": "admin",
        "junior_admin": "junior_admin",
        "moder": "moder",
        "junior_moder": "junior_moder",
        "teacher": "teacher",
        "student": "student",
    }

    role = role_map.get(role_input.lower())

    if not role:
        await message.answer("❌ Такой должности нет.")
        return

    create_user(message.from_user.id, message.from_user)
    users[str(message.from_user.id)]["role"] = role
    save_users()

    await message.answer(f"✅ Должность восстановлена: {role_label(role)}")

# ============================================================
# ЗАПУСК
# ============================================================

async def main():

    bot = Bot(token=BOT_TOKEN)

    print("🤖 Бот запущен!")
    print("🌐 Языки: RU / UZ / EN")
    print("🎓 Классы: 1А–11А/Б")
    print("📅 Расписание: 6Б / 7А / 8А / 8Б")

    runner = await start_web_server(bot)
    try:
        await dp.start_polling(bot)
    finally:
        await runner.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
