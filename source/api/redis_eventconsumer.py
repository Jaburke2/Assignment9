import json
import logging
import redis

from source import config
from Domain import commands
from services import handlers

logger = logging.getLogger(__name__)

r = redis.Redis(**config.get_redis_host_and_port())


def main():
    logger.info("Redis pubsub starting")
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe("bookmarks")

    for m in pubsub.listen():
        handle_message(m)


def handle_message(m):
    logger.info("handling %s", m)
    data = json.loads(m["data"])
    cmd_type = data.get("type")
    if cmd_type == "add_bookmark":
        cmd = commands.AddBookmarkCommand(**data["payload"])
        handlers.add_bookmark(cmd)
    elif cmd_type == "edit_bookmark":
        cmd = commands.EditBookmarkCommand(**data["payload"])
        handlers.edit_bookmark(cmd)
    elif cmd_type == "delete_bookmark":
        cmd = commands.DeleteBookmarkCommand(**data["payload"])
        handlers.delete_bookmark(cmd)


if __name__ == "__main__":
    main()
