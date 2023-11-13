from app import db


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(500), index=True, unique=True)
    start_date = db.Column(db.DateTime)
    duration = db.Column(db.Integer)
    rent = db.Column(db.Float)


class Incomes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), index=True)
    amount = db.Column(db.Float)


class expenditures(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), index=True)
    amount = db.Column(db.Float)


class goal_class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_goal = db.Column(db.Integer)
