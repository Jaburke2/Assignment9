import unittest
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from source.Adapters.orm import bookmarks, Base, start_mappers
from source.Domain.model import BookmarkModel
from sqlalchemy import create_engine

# Assuming date_string is in the format "YYYY-MM-DD"
date_string = "2023-04-08"
date_object = datetime.strptime(date_string, "%Y-%m-%d").date()

class TestORM(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        engine = create_engine('sqlite:///bookmarks.db')
        Session = sessionmaker(bind=engine)
        cls.session = Session()
        Base.metadata.create_all(bind=engine)
        start_mappers()

    def setUp(self):
        self.session.query(BookmarkModel).delete()





    def test_create_bookmark(self):
        bookmark = BookmarkModel(title="Test Bookmark", url="http://test.com", 
                            notes="This is a test bookmark", date_added=date_object, date_edited=date_object)
        self.session.add(bookmark)
        self.session.commit()

        result = self.session.query(BookmarkModel).filter_by(title="Test Bookmark").first()
        self.assertEqual(bookmark, result)
        self.session.delete(result)
        self.session.commit()




    def test_retrieve_bookmark(self):
        bookmark = BookmarkModel(title="Test Bookmark", url="http://test.com", 
                            notes="This is a test bookmark", date_added=date_object, date_edited=date_object)
        self.session.add(bookmark)
        self.session.commit()

        result = self.session.query(BookmarkModel).filter_by(title="Test Bookmark").first()
        self.assertEqual(bookmark, result)
        self.session.delete(result)
        self.session.commit()




    def test_update_bookmark(self):
        bookmark = BookmarkModel(title="Test Bookmark", url="http://test.com", 
                            notes="This is a test bookmark", date_added=date_object, date_edited=date_object)
        self.session.add(bookmark)
        self.session.commit()

        bookmark.notes = "This is an updated test bookmark"
        bookmark.date_edited =date_object
        self.session.commit()

        result = self.session.query(BookmarkModel).filter_by(title="Test Bookmark").first()
        self.assertEqual(bookmark, result)
        self.session.delete(result)
        self.session.commit()




    def test_delete_bookmark(self):
            bookmark = BookmarkModel(title="Test Bookmark", url="http://test.com", 
                                 notes="This is a test bookmark", 
                                 date_added=date_object, date_edited=date_object)
            self.session.add(bookmark)
            self.session.commit()

            self.session.delete(bookmark)
            self.session.commit()
            self.session.rollback()

            result = self.session.query(BookmarkModel).filter_by(title="Test Bookmark").first()
            self.assertIsNone(result)





    @classmethod
    def tearDownClass(cls):
        cls.session.close()
        engine = cls.session.get_bind()
        engine.dispose()
        Base.metadata.drop_all(bind=engine)

if __name__ == '__main__':
    unittest.main()