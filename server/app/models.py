from .extensions import db


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    md5 = db.Column(db.Text())
    token = db.Column(db.Text())
    tag = db.Column(db.Text())
    
    def __init__(self, md5, token, tag=''):
        self.md5 = md5
        self.token = token
        self.tag = tag

    def __repr__(self):
        return '<md5 {0}>'.format(self.md5)

