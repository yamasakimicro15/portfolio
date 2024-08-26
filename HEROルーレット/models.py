from app import db
from datetime import datetime

# データベースモデルの定義
class FortuneHistory(db.Model):
    __tablename__ = 'fortune_history'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    birthdate = db.Column(db.String(10), nullable=False)
    zodiac_sign = db.Column(db.String(10), nullable=False)
    fortune = db.Column(db.String(20), nullable=False)
    lucky_item = db.Column(db.String(20), nullable=False)
    warning = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<FortuneHistory {self.name} - {self.fortune}>'
