from sqlalchemy import (Table, Column, Integer, String, Date, Text)
from sqlalchemy.orm import registry, relationship
import Domain.model as model
import logging
mapper_registry = registry()

Base = mapper_registry.generate_base()

logger = logging.getLogger(__name__)
metadata = mapper_registry.metadata

"""
Pure domain bookmark:
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL,
url TEXT NOT NULL,
notes TEXT,
date_added TEXT NOT NULL
date_edited TEXT NOT NULL
"""
bookmarks = Table(
    "bookmarks",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(255), unique=True),
    Column("url", String(255)),
    Column("notes", Text),
    Column("date_added", Date),
    Column("date_edited", Date),
)

def start_mappers():
    logger.info("starting mappers")
    mapper_registry.map_imperatively(model.Bookmark, bookmarks)