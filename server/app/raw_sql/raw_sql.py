from app import db


def count_all(model):
    res = db.engine.execute("select COUNT(*) from %s" % model.__tablename__)
    names = [row[0] for row in res]
    return names[0]
