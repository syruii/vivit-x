import sqlite3
import random

DATABASE = 'quotes.db'


def _query_db(query, args=(), one=False):
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    cur = db.execute(query, args)
    rv = cur.fetchall()
    success = cur.rowcount
    db.commit()
    cur.close()
    return ((rv[0], success) if rv else None) if one else (rv, success)


def add_quote(message,author,_id):
    (a,success) = _query_db('INSERT OR IGNORE INTO Quote(Author, ID, Content) VALUES((?), (?), (?))', [author, _id, message])
    return success

# TODO: Add searching quote functionality, and specifying a quote
def get_quote(author):
    (quotes,success) = _query_db ('SELECT * FROM Quote WHERE Author = (?)', [author])
    if quotes:
        rand = random.randrange(0,len(quotes))
        return quotes[rand]['Content'], quotes[rand]['ID']
    else:
        return None, None


def del_quote(_id):
    (a,success) = _query_db('DELETE FROM Quote WHERE ID = (?)', [_id])
    return success
