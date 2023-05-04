from __future__ import annotations

from dataclasses import asdict
from typing import TYPE_CHECKING, Callable, Dict, List, Type

from sqlalchemy import select, text, desc
from datetime import datetime

from Domain import commands, events, model
from Domain.commands import EditBookmarkCommand
from Domain.events import BookmarkEdited

if TYPE_CHECKING:
    from . import unit_of_work


def add_bookmark(
    cmd: commands.AddBookmarkCommand,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        bookmark = uow.bookmarks.find_first(
            select(model.Bookmark).where(model.Bookmark.title == cmd.title)
        )
        if bookmark is None:
            date_added = datetime.now()
            bookmark = model.Bookmark(
                id=cmd.id,
                title=cmd.title,
                url=cmd.url,
                notes=cmd.notes,
                date_added=date_added,
                date_edited=date_added,
            )
            uow.bookmarks.add_one(bookmark)


def list_bookmark(
        id: int,
        uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        bookmark = uow.bookmarks.get(id)
        if bookmark is None:
            return 'No results'
        else:
            return bookmark._asdict()


def list_bookmarks(
    cmd: commands.ListBookmarksCommand,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        bookmarks = uow.bookmarks.find_all(
            get_query(cmd.filter, cmd.value, cmd.order_by, cmd.order)
        )
        cmd.bookmarks = [bookmark._asdict() for bookmark in bookmarks]


def edit_bookmark(
    cmd: commands.EditBookmarkCommand,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        bookmark = uow.bookmarks.get(id=cmd.id)
        if bookmark is None:
            raise Exception(f"{cmd.id} was not found")
        bookmark = bookmark._asdict()
        bookmark.update(
            {k: v for k, v in asdict(cmd).items() if v is not None},
            date_edited=datetime.now(),
        )
        uow.bookmarks.update(model.Bookmark(**bookmark))


def delete_bookmark(
    cmd: commands.DeleteBookmarkCommand,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        bookmark = model.Bookmark(id=cmd.id)
        uow.bookmarks.delete_one(bookmark)


def get_query(
    filter: str,
    value: object,
    sort: str,
    order: str,
):
    query = select(model.Bookmark)
    if filter is not None:
        if filter == "id":
            query = query.where(model.Bookmark.id == int(value))
        elif filter == "title" and isinstance(value, str):
            query = query.where(model.Bookmark.title == str(value))
        elif filter == "date_added" and isinstance(value, datetime):
            query = query.where(model.Bookmark.date_added == datetime(value))
        elif filter == "date_edited" and isinstance(value, datetime):
            query = query.where(model.Bookmark.date_edited == datetime(value))
    else:
        query = query.where(model.Bookmark.id.isnot(None))
    if sort is not None:
        if sort == "id":
            query = query.order_by(desc(model.Bookmark.id))
        elif sort == "title":
            query = query.order_by(desc(model.Bookmark.title))
        elif sort == "date_added":
            query = query.order_by(model.Bookmark.date_added)
        elif sort == "date_edited":
            query = query.order_by(model.Bookmark.date_edited)
    if order is not None and order.lower() == "asc":
        query = query.reverse()
    return query
