# import sqlite3
# import pytest

# import blog.db


# # Within an application context, get_db should return
# # the same connection each time it’s called.
# # After the context, the connection should be closed.
# def test_get_close_db(app):
#     with app.app_context():
#         db = blog.db.get_db()
#         # Make sure the db was cached
#         assert db is blog.db.get_db()

#     with pytest.raises(sqlite3.ProgrammingError) as e:
#         db.execute('SELECT 1')

#     assert 'closed' in str(e.value)
