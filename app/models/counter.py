from app import db

class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer)

    def add(self):
        self.status += 1
        return self.status
    def sub(self):
        self.status -= 1
        return self.status

    def __repr__(self):
        return '<Status %r>' % (self.status)