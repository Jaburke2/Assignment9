# pylint: disable=redefined-outer-name
import pytest
import requests
from sqlalchemy.orm import clear_mappers
from source import bootstrap, config
from Domain import commands
from Adapters import notifications
from services import unit_of_work
from ..random_refs import random_bookmark


@pytest.fixture
def bus(sqlite_session_factory):
    bus = bootstrap.bootstrap(
        start_orm=True,
        uow=unit_of_work.SqlAlchemyUnitOfWork(sqlite_session_factory),
        notifications=notifications.EmailNotifications(),
        publish=lambda *args: None,
    )
    yield bus
    clear_mappers()


def get_email_from_mailhog(bookmark):
    host, port = map(config.get_email_host_and_port().get, ["host", "http_port"])
    all_emails = requests.get(f"http://{host}:{port}/api/v2/messages").json()
    return next(m for m in all_emails["items"] if bookmark in str(m))

