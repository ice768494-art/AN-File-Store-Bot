
import asyncio
import json
import os
from bot import Bot, web_app
from pyrogram import compose

# Static default fallback message templates (can be overridden per setup entry if needed)
default_messages = {
    'START': '<blockquote expandable>__Lorem ipsum dolor sit amet,\nconsectetur adipiscing elit sed.\nVivamus luctus urna sed urna.\nCurabitur blandit tempus porttitor.\nNullam quis risus eget urna.__</blockquote>',
    'FSUB': '',
    'ABOUT': 'ABOUT MSG',
    'REPLY': 'reply_text',
    'START_PHOTO': '',
    'FSUB_PHOTO': ''
}

async def main():
    app = []

    # Load and validate setup.json before starting any network clients.
    setup_path = os.environ.get("SETUP_FILE", "setup.json")
    try:
        with open(setup_path, "r", encoding="utf-8") as f:
            setups = json.load(f)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {setup_path} at line {exc.lineno}, column {exc.colno}: {exc.msg}") from exc
    except FileNotFoundError as exc:
        raise SystemExit(f"Configuration file not found: {setup_path}") from exc

    if not isinstance(setups, list) or not setups:
        raise SystemExit("setup.json must contain a non-empty JSON list of bot configurations.")

    required = ("session", "token", "api_id", "api_hash", "db_uri", "db_name", "db", "workers", "admins", "fsubs", "auto_del", "protect", "disable_btn")
    for index, cfg in enumerate(setups, start=1):
        if not isinstance(cfg, dict):
            raise SystemExit(f"Bot configuration #{index} must be a JSON object.")
        missing = [key for key in required if key not in cfg]
        if missing:
            raise SystemExit(f"Bot configuration #{index} is missing: {', '.join(missing)}")
        blank = [key for key in ("token", "api_id", "api_hash", "db_uri", "db_name") if not str(cfg[key]).strip()]
        if blank:
            raise SystemExit(f"Configure these values in {setup_path} (bot #{index}): {', '.join(blank)}")
        try:
            cfg["api_id"] = int(cfg["api_id"])
            cfg["db"] = int(cfg["db"])
            cfg["workers"] = int(cfg["workers"])
            cfg["auto_del"] = int(cfg["auto_del"])
        except (TypeError, ValueError) as exc:
            raise SystemExit(f"Bot configuration #{index}: api_id, db, workers, and auto_del must be integers.") from exc
        if cfg["workers"] < 1:
            raise SystemExit(f"Bot configuration #{index}: workers must be at least 1.")
        if not isinstance(cfg["admins"], list) or not isinstance(cfg["fsubs"], list):
            raise SystemExit(f"Bot configuration #{index}: admins and fsubs must be JSON lists.")

    # Loop through each bot setup config
    for config in setups:
        session = config["session"]
        workers = config["workers"]
        db = config["db"]
        fsubs = config["fsubs"]
        token = config["token"]
        admins = config["admins"]
        messages = config.get("messages", default_messages)
        auto_del = config["auto_del"]
        db_uri = config["db_uri"]
        db_name = config["db_name"]
        api_id = config["api_id"]
        api_hash = config["api_hash"]
        protect = config["protect"]
        disable_btn = config["disable_btn"]

        app.append(
            Bot(
                session,
                workers,
                db,
                fsubs,
                token,
                admins,
                messages,
                auto_del,
                db_uri,
                db_name,
                api_id,
                api_hash,
                protect,
                disable_btn
            )
        )

    await compose(app)


async def runner():
    await asyncio.gather(
        main(),
        web_app()
    )

asyncio.run(runner())
