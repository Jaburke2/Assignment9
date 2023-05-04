import pytest
from datetime import datetime

from Domain import commands, events, model
import services
from services.unit_of_work import FakeUnitOfWork


@pytest.fixture
def uow():
    return FakeUnitOfWork()


def test_add_bookmark(uow):
    cmd = commands.AddBookmarkCommand(
        id=1,
        title="Test Bookmark",
        url="http://www.example.com",
        notes="This is a test bookmark.",
    )
    services.add_bookmark(cmd, uow)

    bookmark = uow.bookmarks.get(1)
    assert bookmark.title == "Test Bookmark"
    assert bookmark.url == "http://www.example.com"
    assert bookmark.notes == "This is a test bookmark."
    assert bookmark.date_added is not None
    assert bookmark.date_edited is not None


def test_add_duplicate_bookmark(uow):
    cmd1 = commands.AddBookmarkCommand(
        id=1,
        title="Test Bookmark",
        url="http://www.example.com",
        notes="This is a test bookmark.",
    )
    cmd2 = commands.AddBookmarkCommand(
        id=2,
        title="Test Bookmark",
        url="http://www.example.com",
        notes="This is a test bookmark.",
    )
    services.add_bookmark(cmd1, uow)
    with pytest.raises(Exception):
        services.add_bookmark(cmd2, uow)


def test_list_bookmarks(uow):
    cmd = commands.AddBookmarkCommand(
        id=1,
        title="Test Bookmark",
        url="http://www.example.com",
        notes="This is a test bookmark.",
    )
    services.add_bookmark(cmd, uow)

    cmd = commands.ListBookmarksCommand(filter="title", value="Test Bookmark")
    services.list_bookmarks(cmd, uow)
    assert len(cmd.bookmarks) == 1
    assert cmd.bookmarks[0]["title"] == "Test Bookmark"


def test_edit_bookmark(uow):
    cmd1 = commands.AddBookmarkCommand(
        id=1,
        title="Test Bookmark",
        url="http://www.example.com",
        notes="This is a test bookmark.",
    )
    services.add_bookmark(cmd1, uow)

    cmd2 = commands.EditBookmarkCommand(
        id=1,
        title="New Title",
        url="http://www.example.com/new",
        notes="This is an updated bookmark.",
    )
    services.edit_bookmark(cmd2, uow)

    bookmark = uow.bookmarks.get(1)
    assert bookmark.title == "New Title"
    assert bookmark.url == "http://www.example.com/new"
    assert bookmark.notes == "This is an updated bookmark."
    assert bookmark.date_edited is not None
    assert bookmark.date_edited > bookmark.date_added


def test_delete_bookmark(uow):
    cmd = commands.AddBookmarkCommand(
        id=1,
        title="Test Bookmark",
        url="http://www.example.com",
        notes="This is a test bookmark.",
    )
    services.add_bookmark(cmd, uow)

    cmd = commands.DeleteBookmarkCommand(id=1)
    services.delete_bookmark(cmd, uow)

    bookmark = uow.bookmarks.get(1)
    assert bookmark is None
