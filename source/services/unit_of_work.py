from datetime import datetime
from unittest.mock import Mock

import pytest

from Domain import commands, events, model
from services import handlers
from unit_of_work import AbstractUnitOfWork


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.bookmarks = Mock()

    def _commit(self):
        pass

    def rollback(self):
        pass


def test_add_bookmark():
    cmd = commands.AddBookmarkCommand(
        id=1,
        title="Test Bookmark",
        url="https://www.testbookmark.com",
        notes="This is a test bookmark",
    )
    uow = FakeUnitOfWork()

    handlers.add_bookmark(cmd, uow)

    uow.bookmarks.add_one.assert_called_once_with(
        model.Bookmark(
            id=1,
            title="Test Bookmark",
            url="https://www.testbookmark.com",
            notes="This is a test bookmark",
            date_added=Mock(),
            date_edited=Mock(),
        )
    )


def test_list_bookmark():
    bookmark = model.Bookmark(
        id=1,
        title="Test Bookmark",
        url="https://www.testbookmark.com",
        notes="This is a test bookmark",
        date_added=datetime.now(),
        date_edited=datetime.now(),
    )
    uow = FakeUnitOfWork()
    uow.bookmarks.get.return_value = bookmark

    result = handlers.list_bookmark(1, uow)

    assert result == bookmark._asdict()


def test_list_bookmarks():
    cmd = commands.ListBookmarksCommand(
        filter=None,
        value=None,
        order_by=None,
        order=None,
    )
    bookmark = model.Bookmark(
        id=1,
        title="Test Bookmark",
        url="https://www.testbookmark.com",
        notes="This is a test bookmark",
        date_added=datetime.now(),
        date_edited=datetime.now(),
    )
    uow = FakeUnitOfWork()
    uow.bookmarks.find_all.return_value = [bookmark]

    handlers.list_bookmarks(cmd, uow)

    assert cmd.bookmarks == [bookmark._asdict()]


def test_edit_bookmark():
    cmd = commands.EditBookmarkCommand(
        id=1,
        title="New Test Bookmark",
        url="https://www.newtestbookmark.com",
        notes="This is a new test bookmark",
    )
    bookmark = model.Bookmark(
        id=1,
        title="Test Bookmark",
        url="https://www.testbookmark.com",
        notes="This is a test bookmark",
        date_added=datetime.now(),
        date_edited=datetime.now(),
    )
    uow = FakeUnitOfWork()
    uow.bookmarks.get.return_value = bookmark

    handlers.edit_bookmark(cmd, uow)

    bookmark_dict = bookmark._asdict()
    bookmark_dict.update(
        {
            "title": "New Test Bookmark",
            "url": "https://www.newtestbookmark.com",
            "notes": "This is a new test bookmark",
            "date_edited": Mock(),
        }
    )
    uow.bookmarks.update.assert_called_once_with(model.Bookmark(**bookmark_dict))


def test_delete_bookmark():
    cmd = commands.DeleteBookmarkCommand(id=1)
    uow = FakeUnitOfWork()

    handlers.delete_bookmark(cmd, uow)

    uow.bookmarks.delete_one.assert_called_once_with(model.Bookmark(id=1))
