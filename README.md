# Advanced Telegram File Store Bot

## Before deployment

This repository is a multi-bot Pyrogram file-store bot. It cannot start until you provide your own Telegram and MongoDB credentials. Never commit real credentials to a public repository.

### 1. Configure `setup.json`

`setup.json` must be a valid JSON **list**. Fill in these fields for each bot entry:

- `session`: a unique session name, for example `file_store_bot`
- `token`: bot token from Telegram's BotFather
- `api_id` and `api_hash`: credentials from Telegram's official developer portal
- `db_uri`: MongoDB connection URI
- `db_name`: MongoDB database name
- `db`: numeric ID of the private database channel, usually beginning with `-100`

The provided file intentionally has blank credentials and `db: null`; replace them with your own values before starting. The bot must be an administrator in the database channel with permission to post messages. It may also need administrator/invite permissions in force-subscription channels.

Keep `fsubs` as a JSON list. Each entry uses `[channel_id, creates_join_request, timer]`. Set `admins` to a list of Telegram numeric user IDs. `auto_del` is in seconds; set it to `0` to disable automatic deletion.

### 2. Set the owner

Set the `OWNER_ID` environment variable to your Telegram numeric user ID. If it is not set, the code retains the original project's default owner ID. Set `PORT` if your hosting provider requires a specific HTTP port; otherwise the default is `8020`.

### 3. Install and run

```bash
python -m pip install -r requirements.txt
python main.py
```

Docker and Procfile deployment are also included. The startup script installs dependencies and then launches the bot. Configure secrets through your host's secret/environment-variable settings when possible, and keep `setup.json` private if it contains credentials.

## Validation performed

The Python files are syntax-compiled and `setup.json` is checked for valid JSON. A live startup still requires valid Telegram credentials, a reachable MongoDB instance, and correct channel permissions.
