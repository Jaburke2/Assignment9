from baseapi import AbstractBookMarkAPI
from Domain import commands
from Adapters import repository, flask_sqlalchemy

import functools

from flask import (Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for,
)
from flask_sqlalchemy import SQLAlchemy
from api.baseapi import AbstractBookMarkAPI

app = Flask(__name__)

class FlaskBookmarkAPI(AbstractBookMarkAPI):
    """
    Flask - the beginnings of a Flask implementation is shown below. 
    Actual action responses would replace the starter methods below.

    """
    def __init__(self) -> None:
        super().__init__()
    

    def index(self):
        # Call the 'ListBookmarks' Command from commands.py
        return commands.ListBookmarksCommand().execute() 

    def one(self, id):
        return f'The provided id is {id}'

    def all(self):
        return f'all records'

    # @app.route('/api/first/<property>/<value>/<sort>')
    def first(self, filter, value, sort):
        return f'the first '
        pass
    
    def many(self, filter, value, sort):
        pass
    
    def add(bookmark):
        # return commands.AddBookmarkCommand().execute(data)
        return f'Add a bookmark'

    def delete(bookmark):
        pass

    def update(bookmark):
        pass

fb = FlaskBookmarkAPI()
bp = Blueprint('flask_bookmark_api', __name__, url_prefix='/api')

# @app.route('/api')
bp.add_url_rule('/', 'index', fb.index, ['GET'])

# @app.route('/api/one/<id>')
bp.add_url_rule('/one/<id>', 'one', fb.one, ['GET'])

# @app.route('/api/all')
bp.add_url_rule('/all', 'all', fb.all, ['GET'])

# @app.route('/api/add')
bp.add_url_rule('/add', 'add', fb.add, ['GET'])