import json
import pytest
from tenacity import Retrying, RetryError, stop_after_delay
from . import api_client, redis_client
from ..random_refs import random_uuid, random_url

@pytest.mark.usefixtures("postgresql_db")
@pytest.mark.usefixtures("restart_api")
@pytest.mark.usefixtures("restart_redis_pubsub")
def test_change_bookmark_url():
    # start with a bookmark
    bookmark_id = random_uuid()
    bookmark_url = random_url()
    api_client.post_to_add_bookmark(bookmark_id, bookmark_url)

    subscription = redis_client.subscribe_to("bookmark_edited")

    # change url of existing bookmark
    new_bookmark_url = random_url()
    redis_client.publish_message(
        "change_bookmark_url",
        {"id": bookmark_id, "url": new_bookmark_url},
    )

    # wait until we see a message saying the bookmark has been edited
    messages = []
    for attempt in Retrying(stop=stop_after_delay(3), reraise=True):
        with attempt:
            message = subscription.get_message(timeout=1)
            if message:
                messages.append(message)
                data = json.loads(messages[-1]["data"])
                assert data["id"] == bookmark_id
                assert data["url"] == new_bookmark_url
