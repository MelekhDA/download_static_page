from app import db

__all__ = [
    'SitePage'
]


class SitePage(db.Model):
    """Table for archiving pages at specified addresses"""

    __tablename__ = 'site_page'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    zipfile = db.Column(db.LargeBinary)
    status = db.Column(db.Integer)

    def __init__(self, url):
        self.url = url
        self.status = 0

    def __repr__(self):
        return '<id {}>'.format(self.id)
