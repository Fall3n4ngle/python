import enum
from extensions import db
from datetime import datetime

class EnumPostType(enum.Enum):
    news = 'news'
    publication = 'publication'
    other = 'other'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    text = db.Column(db.String(1000))
    image = db.Column(db.String, default='postdefault.jpg')
    created = db.Column(db.DateTime, default=datetime.utcnow())
    enabled = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    type = db.Column(db.Enum(EnumPostType), default=EnumPostType.other.value)

    def __repr__(self):
        return f"Post(id={self.id}, title='{self.title}')"
